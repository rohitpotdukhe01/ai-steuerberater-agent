"""Tools for managing tax prep state and generating checklists."""

from __future__ import annotations

from typing import Any, Literal

from google.adk.tools import ToolContext

from .knowledge import BASE_DOCUMENTS, DEDUCTION_CATALOG, QUESTION_BANK

AppState = dict[str, Any]


def _ensure_state(tool_context: ToolContext) -> AppState:
    state = tool_context.state
    if "profile" not in state:
        state["profile"] = {}
    if "expenses" not in state:
        state["expenses"] = []
    if "documents" not in state:
        state["documents"] = []
    if "notes" not in state:
        state["notes"] = []
    if "reviewed_categories" not in state:
        state["reviewed_categories"] = []
    return state


def save_profile_field(field: str, value: Any, tool_context: ToolContext) -> dict:
    """Save a user profile field in session state."""
    state = _ensure_state(tool_context)
    profile = state["profile"]
    profile[field] = value
    return {"status": "saved", "field": field, "value": value}


def add_expense(
    category: str,
    description: str,
    amount_eur: float | None,
    tool_context: ToolContext,
) -> dict:
    """Record a potential expense or deduction-related item."""
    state = _ensure_state(tool_context)
    entry = {
        "category": category,
        "description": description,
        "amount_eur": amount_eur,
    }
    state["expenses"].append(entry)
    return {"status": "added", "expense": entry}


def add_document(name: str, reason: str | None, tool_context: ToolContext) -> dict:
    """Record a document the user should gather."""
    state = _ensure_state(tool_context)
    doc = {"name": name, "reason": reason}
    state["documents"].append(doc)
    return {"status": "added", "document": doc}


def add_note(note: str, tool_context: ToolContext) -> dict:
    state = _ensure_state(tool_context)
    state["notes"].append(note)
    return {"status": "added", "note": note}


def mark_category_reviewed(category_id: str, tool_context: ToolContext) -> dict:
    state = _ensure_state(tool_context)
    reviewed = state["reviewed_categories"]
    if category_id not in reviewed:
        reviewed.append(category_id)
    return {"status": "reviewed", "category_id": category_id}


def get_reviewed_categories(tool_context: ToolContext) -> dict:
    state = _ensure_state(tool_context)
    return {"reviewed_categories": state["reviewed_categories"]}


def get_profile(tool_context: ToolContext) -> dict:
    state = _ensure_state(tool_context)
    return state["profile"]


def get_deduction_catalog() -> dict:
    """Return the full deduction catalog used for guidance."""
    return {"categories": DEDUCTION_CATALOG}


def _evaluate_applicability(
    applies_if: list[dict], profile: dict
) -> Literal["applicable", "unknown", "not_applicable"]:
    if not applies_if:
        return "unknown"
    unknown = False
    for rule in applies_if:
        field = rule.get("field")
        values = rule.get("values", [])
        if field not in profile:
            unknown = True
            continue
        if profile.get(field) not in values:
            return "not_applicable"
    return "unknown" if unknown else "applicable"


def build_personalized_checklist(tool_context: ToolContext) -> dict:
    """Classify categories into applicable/unknown based on the profile."""
    state = _ensure_state(tool_context)
    profile = state["profile"]
    applicable = []
    unknown = []
    not_applicable = []
    for category in DEDUCTION_CATALOG:
        status = _evaluate_applicability(category.get("applies_if", []), profile)
        if status == "applicable":
            applicable.append(category)
        elif status == "not_applicable":
            not_applicable.append(category)
        else:
            unknown.append(category)
    return {
        "applicable": applicable,
        "unknown": unknown,
        "not_applicable": not_applicable,
    }


def get_missing_questions(tool_context: ToolContext) -> dict:
    state = _ensure_state(tool_context)
    profile = state["profile"]
    missing = []
    for entry in QUESTION_BANK:
        field = entry["field"]
        if field not in profile:
            missing.append(entry["question"])
    return {"missing_questions": missing}


def generate_document_checklist(tool_context: ToolContext) -> dict:
    state = _ensure_state(tool_context)
    profile = state["profile"]
    documents = list(BASE_DOCUMENTS)

    if profile.get("employment_type") in {"employee", "public_servant"}:
        documents.append("Work-related expense receipts and logs")

    if profile.get("employment_type") in {"self_employed", "freelancer"}:
        documents.append("Business income and expense ledger")

    if profile.get("has_children") is True:
        documents.append("Childcare invoices and proof of payment")

    if profile.get("has_rental_property") is True:
        documents.append("Rental income statements and repair invoices")

    if profile.get("has_investments") is True:
        documents.append("Annual bank/broker tax statements")

    return {"document_checklist": documents}


def summarize_case(tool_context: ToolContext) -> dict:
    state = _ensure_state(tool_context)
    profile = state["profile"]
    checklist = build_personalized_checklist(tool_context)
    missing = get_missing_questions(tool_context)["missing_questions"]
    documents = generate_document_checklist(tool_context)["document_checklist"]

    return {
        "profile": profile,
        "potential_categories": {
            "applicable": [c["name"] for c in checklist["applicable"]],
            "unknown": [c["name"] for c in checklist["unknown"]],
        },
        "missing_questions": missing,
        "document_checklist": documents,
        "expenses_recorded": state["expenses"],
        "notes": state["notes"],
        "reviewed_categories": state["reviewed_categories"],
    }
