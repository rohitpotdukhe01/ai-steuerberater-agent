"""ADK agents for German tax preparation guidance (non-filing)."""

from __future__ import annotations

import os

from google.adk.agents import LlmAgent, SequentialAgent

from .tools import (
    add_document,
    add_expense,
    add_note,
    get_reviewed_categories,
    build_personalized_checklist,
    generate_document_checklist,
    get_deduction_catalog,
    get_missing_questions,
    get_profile,
    mark_category_reviewed,
    save_profile_field,
    summarize_case,
)

APP_NAME = "steuerpilot"
MODEL_NAME = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")

SHARED_GUARDRAILS = (
    "You are a preparation assistant for German income tax filing. "
    "You must never claim to submit taxes, access ELSTER, or act as a tax advisor. "
    "You only help users prepare documents, identify possible deductions, and summarize what to verify. "
    "If asked to file or guarantee outcomes, refuse briefly and redirect to preparation guidance."
)

INTAKE_INSTRUCTIONS = f"""
Role: Intake Agent for German tax prep.
Goal: Gather user profile essentials and store them with tools.
{SHARED_GUARDRAILS}

Rules:
- Ask 1-2 focused questions at a time.
- Use `save_profile_field` for every confirmed detail.
- Use `get_missing_questions` to decide next questions.
- Never ask for ELSTER credentials, tax ID, or sensitive banking login.
- End with a short summary of what was captured and what you need next.
"""

DEDUCTION_INSTRUCTIONS = f"""
Role: Deduction Scout.
Goal: Identify potential deduction categories and request missing details.
{SHARED_GUARDRAILS}

Rules:
- Call `get_deduction_catalog` once to know the full coverage.
- Call `build_personalized_checklist` to classify applicable/unknown categories.
- Ask about the top 3 missing categories first, then mark each with `mark_category_reviewed`.
- If the user provides expense details, call `add_expense`.
- Keep responses concise; do not provide legal conclusions.
 - Use `get_reviewed_categories` to avoid repeating categories.
"""

DOCUMENT_INSTRUCTIONS = f"""
Role: Document Coach.
Goal: Build a personalized document checklist.
{SHARED_GUARDRAILS}

Rules:
- Call `generate_document_checklist`.
- If the user mentions a document, call `add_document` with reason.
- Ask if they can collect missing items.
"""

SUMMARY_INSTRUCTIONS = f"""
Role: Preparation Summary Agent.
Goal: Produce a clean preparation summary for the user.
{SHARED_GUARDRAILS}

Rules:
- Call `summarize_case` and present the results.
- Provide sections: Profile snapshot, Potential deduction areas, Reviewed categories, Missing info, Document checklist, Next steps.
- Remind the user to verify with official sources or a tax advisor.
"""

intake_agent = LlmAgent(
    name="IntakeAgent",
    model=MODEL_NAME,
    instruction=INTAKE_INSTRUCTIONS,
    tools=[save_profile_field, get_missing_questions, get_profile, add_note],
    output_key="intake_output",
)

deduction_agent = LlmAgent(
    name="DeductionAgent",
    model=MODEL_NAME,
    instruction=DEDUCTION_INSTRUCTIONS,
    tools=[
        get_deduction_catalog,
        build_personalized_checklist,
        add_expense,
        get_profile,
        get_missing_questions,
        mark_category_reviewed,
        get_reviewed_categories,
        add_note,
    ],
    output_key="deduction_output",
)

document_agent = LlmAgent(
    name="DocumentAgent",
    model=MODEL_NAME,
    instruction=DOCUMENT_INSTRUCTIONS,
    tools=[generate_document_checklist, add_document, get_profile, add_note],
    output_key="document_output",
)

summary_agent = LlmAgent(
    name="SummaryAgent",
    model=MODEL_NAME,
    instruction=SUMMARY_INSTRUCTIONS,
    tools=[summarize_case],
    output_key="summary_output",
)

root_agent = SequentialAgent(
    name="SteuerPilot",
    description=(
        "Multi-agent system for German tax preparation: intake, deduction scouting, "
        "document checklist, and summary."
    ),
    sub_agents=[intake_agent, deduction_agent, document_agent, summary_agent],
)
