# Core Constraints & Governance Rules

These 20 rules govern all AI architect and developer behavior across every phase of the project:

1. **Immutable Logging (Never Overwrite):** You are strictly forbidden from editing or overwriting past plans, checkpoints, audits, or chat logs. Always create a NEW sequentially numbered file (e.g., `02_plans/01_PHASE_1_PLAN.md`, `04_audits/AUDIT_001.md`, `05_chat_logs/LOG_001_decisions.md`).
2. **Record Everything:** Any significant conversation, decision, or shift in context must be recorded as a new file in `05_chat_logs/` before ending a session.
3. **Draft Before Writing:** Before writing any code, draft a detailed plan for the current phase in chat. Stop and ask for feedback or approval. Do not write this to the file system yet.
4. **Iterate and Lock:** If changes are requested, update the draft in chat. Once explicitly approved, write it as a new immutable file in `02_plans/` (e.g., `01_PHASE_1_PLAN.md`).
5. **Execute Phase:** Only after the approved plan is saved to `02_plans/`, write code or implement changes strictly for that specific phase.
6. **Audit and Verify:** After execution, verify work against phase requirements. Create a new audit log in `04_audits/` detailing additions, changes, and test results.
7. **Strict Stop and Wait:** Explicitly forbidden from moving to the next phase automatically. Stop, present the Audit report, and ask: "Phase complete and audited. Please verify the changes. Shall we lock this phase and proceed?"
8. **Lock and Checkpoint:** Only after user replies "Approved", generate a new checkpoint file in `03_checkpoints/`, update `CURRENT_STATE.md` (the only overwriteable tracking file), and draft the new plan for the next phase in chat.
9. **Continuous Git Versioning:** Provide exact `git add` and `git commit -m` commands after any working sub-step or phase.
10. **Human-Readable Code:** Clean, modular, properly formatted code with clear variable names and inline comments explaining the *why*, not just the *what*.
11. **Repository Onboarding Files:** Generate and maintain public onboarding files (`README.md`, `CONTRIBUTING.md`).
12. **Session Pause and Handoff:** If paused while a phase plan is pending, save draft to `02_plans/PENDING_NEXT_PHASE_DRAFT.md` and log pause in `CURRENT_STATE.md`. On resumption, load and present for approval.
13. **Optimized Context Loading (Read Order):** Read strictly in order: `AI_ENTRY_READ_ME_FIRST.md` -> `.ai/01_rules/` -> `CURRENT_STATE.md` -> newest checkpoint -> `PENDING_NEXT_PHASE_DRAFT.md`.
14. **No Blind Edits:** Never modify existing files without reading their current contents in the active session.
15. **Dependency Tracking:** Update dependency files immediately when introducing libraries and note in Audit.
16. **Error Loop Escalation:** Stop after 3 consecutive failed fix attempts, document the error, and escalate.
17. **Anti-Scope Creep:** Confine changes strictly to the active phase. No unsolicited refactoring.
18. **Zero Secrets Policy:** Never hardcode credentials. Enforce `.env` and `.gitignore`.
19. **Execution Validation:** Execute code, compile, or run tests in terminal before presenting Audit reports.
20. **The Rollback Protocol:** On "Initiate Rollback", stop, revert to last Git commit, update `CURRENT_STATE.md`, and ask which checkpoint to return to.
