# Phase-Gate Protocol

## The 6-Step Phase Execution Lifecycle

```
[Phase Draft in Chat]
        │
        ▼ (User Feedback & Iteration)
[User Approves Draft]
        │
        ▼
[Write 02_plans/XX_PHASE_X_PLAN.md]
        │
        ▼
[Implement Code Strictly within Phase Scope]
        │
        ▼
[Run Automated Unit / Integration / E2E Tests]
        │
        ▼
[Generate Audit Report in 04_audits/AUDIT_XXX.md]
        │
        ▼
[Present Audit & Ask: "Phase complete and audited. Please verify the changes. Shall we lock this phase and proceed?"]
        │
        ▼ (User responds "Approved")
[Create 03_checkpoints/CHECKPOINT_XXX.md]
        │
        ▼
[Update CURRENT_STATE.md & Git Commit Recommendation]
        │
        ▼
[Draft Next Phase in Chat]
```

## Transition Rules
- No code may be written before the plan is formally saved in `02_plans/`.
- No phase may be closed without an audit report and green test suite.
- Advancing to the next phase requires explicit user authorization.
