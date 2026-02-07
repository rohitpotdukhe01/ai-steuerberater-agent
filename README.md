# SteuerPilot — AI Agents for German Tax Prep (Portfolio Demo)

SteuerPilot is a portfolio project that showcases a multi-agent system for **preparing** German income tax filing. It does **not** submit taxes or integrate with ELSTER. Instead, it helps users gather the right inputs, surface missed deductions, and produce a clean preparation summary.

## Why would anyone use this instead of Taxfix or ELSTER?

- **Taxfix** focuses on filing. SteuerPilot stays in prep mode: it builds an evidence-first checklist and a structured summary you can file yourself or hand to a tax advisor.
- **ELSTER** is the official portal. SteuerPilot is the companion that reduces friction before you log in.
- **Differentiator:** a transparent, multi-agent workflow that checks *every deduction category* and documents needed, without asking for ELSTER credentials.

## What this demo delivers

- Guided intake that captures all relevant profile details.
- A comprehensive deduction radar (based on categories, not legal guarantees).
- Personalized document checklist.
- Export-ready summary for filing.

> Disclaimer: This is **not tax advice** and not an official filing tool. Always verify with official sources or a tax advisor.

---

## Architecture

The system uses **Google Agent ADK** with a multi-agent workflow:

1. **Intake Agent** — collects core profile info.
2. **Deduction Agent** — scans all deduction categories and asks for missing details.
3. **Document Agent** — builds a personalized evidence checklist.
4. **Summary Agent** — produces a prep-ready summary.

The agents are orchestrated as a **SequentialAgent** with shared session state so each step builds on prior info.

---

## Local setup

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Configure API key

```bash
export GOOGLE_API_KEY="YOUR_KEY_HERE"
```

### 3. Run the demo server

```bash
python main.py
```

Open: `http://localhost:8080`

---

## Replit deployment

1. Create a new Replit project from this repo.
2. Add a secret: `GOOGLE_API_KEY`.
3. Set the run command to:

```bash
python main.py
```

Replit will expose the app on port 8080.

---

## Project structure

- `main.py` — FastAPI app for the demo UI + chat endpoint.
- `src/ai_steuerberater_agent/agent.py` — ADK agent system.
- `src/ai_steuerberater_agent/tools.py` — stateful tools and checklist logic.
- `src/ai_steuerberater_agent/knowledge.py` — deduction categories and questions.
- `static/` — portfolio frontend.

---

## Notes on safety

- The system **never** asks for ELSTER credentials or files taxes.
- The UI and instructions emphasize preparation and verification.
- All outputs are guidance-only and should be validated.
