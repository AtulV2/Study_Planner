# Contributing to AutoPace (ResilientCal)

Thank you for contributing to **AutoPace**! This project is maintained under strict software craftsmanship standards to ensure zero defect rates and mathematical reliability.

---

## 🏛️ Phase-Gate Execution Protocol

All engineering changes must follow the 6-step lifecycle documented in `.ai/01_rules/02_PHASE_GATE_PROTOCOL.md`:

1. **Draft Plan First:** Propose changes in detail before altering code.
2. **Immutable Planning:** Approved plans are recorded sequentially under `.ai/02_plans/`.
3. **Targeted Implementation:** Code changes must be strictly confined to the active phase scope. No unsolicited refactoring of unrelated modules.
4. **Automated Verification:** 100% of Pytest unit and integration tests must pass prior to closing a phase.
5. **Mandatory Audit:** Every phase must conclude with an audit report in `.ai/04_audits/` logging all additions, test outputs, and contract conformance.
6. **Immutable Checkpoints:** Locked state is recorded in `.ai/03_checkpoints/`.

---

## 📐 Code & Design Craftsmanship Standards

- **Zero Placeholders:** Never commit `# TODO`, `pass`, or mock stubs in production services. Every function must be fully implemented.
- **Explain the "Why":** Add clean inline comments explaining mathematical decisions (interval arithmetic, buffer injections, bedtime cascade) rather than obvious syntax.
- **Strict Typing:** All FastAPI endpoints require Pydantic v2 schemas; all database entities require SQLAlchemy 2.0 type-annotated mapped columns.
- **Zero Secrets:** Never hardcode credentials, API tokens, or database connection strings. Use environment variables via `.env`.

---

## 🧪 Running Tests Locally

Before submitting a Pull Request, run the complete test suite:

```bash
# Run backend tests
python -m pytest backend/tests -v

# Verify frontend production build
cd frontend
npm run build
```
Ensure 100% of tests pass and the production bundle compiles with zero errors.
