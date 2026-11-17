# AI Entry Protocol (Read Me First)

Welcome to the **AutoPace (ResilientCal)** project.
This repository operates under a strict **Phase-Gate Governance Protocol** to prevent context loss, regressions, and scope creep across sessions and AI models.

## Mandatory Entry Read Sequence
When entering any new session, you MUST read files strictly in this order:
1. `AI_ENTRY_READ_ME_FIRST.md` (This file)
2. `.ai/01_rules/01_CORE_CONSTRAINTS.md`
3. `.ai/01_rules/02_PHASE_GATE_PROTOCOL.md`
4. `.ai/01_rules/03_AUDIT_VERIFICATION.md`
5. `.ai/CURRENT_STATE.md`
6. The single most recent file in `.ai/03_checkpoints/`
7. `.ai/02_plans/PENDING_NEXT_PHASE_DRAFT.md` (if it exists)

> [!WARNING]
> Do NOT read historical files in `.ai/04_audits/`, `.ai/05_chat_logs/`, or older checkpoints unless explicitly commanded to retrieve specific past context.

## Non-Negotiable Core Principles
- **Never overwrite history**: Past plans, checkpoints, audits, and chat logs are immutable. Always generate sequentially numbered files.
- **Draft in chat before writing**: Never write code or lock plans without explicit user approval.
- **Strict Stop and Wait**: Never advance to the next phase automatically. Always stop, present the Audit report, and await explicit user approval.
- **Continuous Git versioning**: Provide exact git add and commit commands after every sub-step or phase.
- **Zero Secrets**: All credentials go into `.env` (which is gitignored).
- **Execution Validation**: Run code/tests in the terminal before presenting audit reports.
