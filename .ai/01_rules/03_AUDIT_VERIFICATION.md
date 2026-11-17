# Audit & Verification Standard

Every phase execution ends with a mandatory audit log saved under `.ai/04_audits/AUDIT_XXX.md`.

## Mandatory Audit Contents
1. **Phase Name & Goal**: Target phase and scope statement.
2. **Files Created & Modified**: Detailed list of all paths touched.
3. **Dependencies Introduced**: Explicit list of added libraries/packages with versions.
4. **Automated Test Results**: Full test run outputs (Pytest / Playwright), pass/fail counts, and coverage.
5. **Contract Conformance**: Verification against `blueprint/04_API_AND_DATA_CONTRACT_SPECIFICATION.md` and `blueprint/02_SYSTEM_ARCHITECTURE_AND_MODULAR_DESIGN.md`.
6. **Defects or Limitations Identified**: Any known trade-offs or remaining edge cases.
7. **Git State**: Recommended commit message and branch status.
