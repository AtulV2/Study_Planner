# 05. Comprehensive Automated Testing Suite & Quality Assurance

---

## 1. Testing Philosophy & Zero-Defect Mandate

To satisfy the requirement that **"after coding, every functionality must work, and every button must work in any edge case,"** the project enforces a three-tier automated verification pipeline:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PLAYWRIGHT END-TO-END (E2E) TESTS                     │
│  - Verifies every button, modal, toggle, form submit, and delete action     │
│  - Validates real browser DOM interactions, canvas rendering & toasts       │
├─────────────────────────────────────────────────────────────────────────────┤
│                    FASTAPI INTEGRATION TESTS (TestClient)                   │
│  - Validates all REST API status codes (200, 201, 204, 400, 404, 422)       │
│  - Validates database cascade deletions and transaction rollbacks           │
├─────────────────────────────────────────────────────────────────────────────┤
│                    PYTEST UNIT TESTS (Domain Algorithms)                    │
│  - Pure function mathematical validation: Interval merging, gap finding    │
│  - Capacity exhaustion, midnight rollovers, triage calculations            │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Quality Mandates:**
1. **No Broken Buttons:** Every clickable element (`button`, `a`, icon trigger) must have an associated Playwright or Vitest test verifying user feedback upon click.
2. **Deterministic Test Isolation:** Tests must never depend on external network access or pre-existing database state. Every test runs against an isolated, in-memory SQLite database.
3. **No Silent HTTP Failures:** The frontend must explicitly handle HTTP 204 (No Content), 400 (Validation), and 500 (Server Error) with immediate user-facing notifications.

---

## 2. Backend Automated Test Suite (Pytest)

### Unit Tests: Gap Engine & Recovery Logic (`tests/unit/`)

#### Test Suite 1: `test_interval_scheduler.py`
* `test_merge_touching_intervals`: Verifies intervals `[09:00-10:00]` and `[10:00-11:00]` merge into `[09:00-11:00]`.
* `test_merge_overlapping_intervals`: Verifies `[09:00-10:30]` and `[10:00-11:30]` merge into `[09:00-11:30]`.
* `test_meal_buffers_injected`: Confirms lunch `[12:30-13:15]` and dinner `[18:30-19:15]` are marked busy even if the calendar has no events.
* `test_capacity_cap_enforced`: When a student has 4 hours already scheduled and the cap is 5.5 hours, scheduling a 2-hour task must be rejected or moved to the next day.
* `test_zero_free_gaps`: When a student's waking day is 100% booked, gap finder returns empty list without raising unhandled exceptions.

#### Test Suite 2: `test_recovery_algorithms.py`
* `test_auto_heal_finds_next_buffer`: Verifies a missed Monday block is rescheduled to Tuesday morning before Wednesday's due date.
* `test_triage_mvp_downscale`: Verifies low-priority deliverables are trimmed by exactly 30% and medium-priority by 20%.
* `test_shift_today_midnight_rollover`: When shifting a block at 22:00 by 2 hours (past 23:00 sleep cutoff), the block rolls over to 08:00 the following morning.
* `test_micro_action_generator`: Verifies recommendation returns a single valid block with duration between 30 and 45 minutes.

### API Integration Tests (`tests/integration/`)

#### Test Suite 3: `test_api_endpoints.py`
* `test_healthcheck_returns_200_and_db_status`
* `test_seed_database_idempotent`: Running `/api/v1/seed` multiple times cleanly resets and re-populates without primary key collision.
* `test_crud_course`: Create -> Read -> Update -> Delete.
* `test_crud_fixed_commitment`: Add lecture -> Verify in weekly list -> Mark missed -> Delete.
* `test_crud_deadline`: Create assignment with estimated hours -> Auto-schedule -> Verify study blocks generated.
* `test_cascade_delete_integrity`:
  - Deleting a `Course` must cleanly delete all child `FixedCommitment` and `Deadline` rows.
  - Deleting a `Deadline` must cleanly delete all child `StudyBlock` rows.
* `test_http_204_delete_contract`: Deleting returns HTTP 204 with empty body; client must not crash on `.json()` parse.

---

## 3. Frontend Automated Test Suite (Vitest + Playwright)

### Component Unit Tests (`frontend/tests/unit/`)
* `test_burnout_meter_color_thresholds`:
  - Under 70% capacity: Emerald green (`#059669`).
  - 70% to 100%: Royal blue (`#2563EB`).
  - Above 100% capacity: Amber alert (`#D97706`) with `"Overload"` badge.
* `test_event_card_toggle`:
  - Clicking complete checkbox fires `onToggleComplete` with correct ID.
  - Card visually updates with strikethrough styling and completed badge.
* `test_modal_form_validation`:
  - Submitting deadline form without title or valid due date displays field errors and prevents API call.

### End-to-End User Flow Tests (`frontend/tests/e2e/autopace.spec.js`)

The Playwright test suite executes the complete user journey in a real Chromium browser:

```javascript
import { test, expect } from '@playwright/test';

test.describe('AutoPace End-to-End Verification Suite', () => {

  test.beforeEach(async ({ page }) => {
    // Navigate and reset to clean seeded demo state
    await page.goto('http://localhost:5173');
    await page.click('button[title*="Reset Seed"]');
    await expect(page.locator('.brand-title')).toHaveText('AutoPace');
  });

  test('1. Every global action button responds and opens respective modal', async ({ page }) => {
    // Test "Class / Event" Modal
    await page.click('button:has-text("Class / Event")');
    await expect(page.locator('.modal-title:has-text("Add Class or Commitment")')).toBeVisible();
    await page.click('button:has-text("Cancel")');
    await expect(page.locator('.modal-container')).toBeHidden();

    // Test "Deadline" Modal
    await page.click('button:has-text("Deadline")');
    await expect(page.locator('.modal-title:has-text("Add Deliverable")')).toBeVisible();
    await page.click('button:has-text("Cancel")');
    await expect(page.locator('.modal-container')).toBeHidden();

    // Test "Recover Schedule" Modal
    await page.click('button:has-text("Recover Schedule")');
    await expect(page.locator('.modal-title:has-text("Recover Schedule")')).toBeVisible();
    await page.click('button:has-text("Close")');
    await expect(page.locator('.modal-container')).toBeHidden();
  });

  test('2. Single-click status toggles update immediately', async ({ page }) => {
    // Find first study block toggle button
    const firstBlockToggle = page.locator('.study-block-card .btn-toggle-complete').first();
    await firstBlockToggle.click();
    
    // Check that card receives completed visual class
    await expect(page.locator('.study-block-card.completed').first()).toBeVisible();
  });

  test('3. Missed session triggers recovery workflow and heals schedule', async ({ page }) => {
    // Mark a block as missed
    const markMissedBtn = page.locator('.study-block-card .btn-mark-missed').first();
    await markMissedBtn.click();

    // Verify recovery alert banner appears
    await expect(page.locator('.recovery-notice-banner')).toBeVisible();

    // Click "Recover Schedule"
    await page.click('.recovery-notice-banner button:has-text("Recover")');
    await expect(page.locator('.recovery-diff-table')).toBeVisible();

    // Apply auto-heal recovery
    await page.click('button:has-text("Apply Recovery Plan")');

    // Verify toast appears and banner disappears
    await expect(page.locator('.toast-success')).toBeVisible();
    await expect(page.locator('.recovery-notice-banner')).toBeHidden();
  });

  test('4. Delete button cleanly removes item and handles HTTP 204 without crash', async ({ page }) => {
    const initialCount = await page.locator('.study-block-card').count();
    
    // Click trash button on first block
    page.on('dialog', dialog => dialog.accept()); // Accept window.confirm if any
    const trashBtn = page.locator('.study-block-card .btn-trash').first();
    await trashBtn.click();

    // Verify block count decremented by 1
    await expect(page.locator('.study-block-card')).toHaveCount(initialCount - 1);
  });

  test('5. Auto-Fit Gaps button allocates pending study sessions', async ({ page }) => {
    await page.click('button:has-text("Auto-Fit Gaps")');
    await expect(page.locator('.toast-success:has-text("allocated")')).toBeVisible();
  });
});
```

---

## 4. Test Execution Instructions

Add these standardized test commands to the project scripts:

### Backend Execution
```bash
# Run all unit and integration tests with coverage report
pytest --maxfail=1 --disable-warnings -v --cov=app tests/
```

### Frontend Execution
```bash
# Run Vitest component tests
npm run test:unit

# Run Playwright end-to-end browser tests
npx playwright test
```
