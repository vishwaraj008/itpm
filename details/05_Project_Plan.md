# Project Plan & Sprint Schedule
## College Event Management System (CEMS)

---

| Field | Details |
|---|---|
| **Document Type** | Project Plan / Sprint Schedule |
| **Project** | College Event Management System |
| **Duration** | 10 Days |
| **Methodology** | Agile Scrum (2-day sprints) |
| **Version** | 1.0 |
| **Date** | 2026-01-28 |

---

## 1. Project Timeline Overview

```
Day  1  2  3  4  5  6  7  8  9 10
     |──────|──────|──────|──────|──────|
     Sprint1 Sprint2 Sprint3 Sprint4 Sprint5
```

| Sprint | Days | Theme |
|---|---|---|
| Sprint 1 | Days 1–2 | Foundation (Setup + Auth) |
| Sprint 2 | Days 3–4 | Core Modules (Events + Budget) |
| Sprint 3 | Days 5–6 | Analytics (Charts + Risk) |
| Sprint 4 | Days 7–8 | AI Features |
| Sprint 5 | Days 9–10 | Export, Testing & Polish |

---

## 2. Sprint 1 — Foundation (Days 1–2)

**Goal**: Working Django project with user authentication and role system

### Tasks

| Task ID | Task | Owner | Est. Hours | Priority |
|---|---|---|---|---|
| S1-01 | Initialize Django project, create virtual env, install dependencies | Dev | 1h | P1 |
| S1-02 | Configure settings.py, .env, database | Dev | 1h | P1 |
| S1-03 | Create Django apps: accounts, events, budget, risks, analytics, ai_features | Dev | 0.5h | P1 |
| S1-04 | Design and implement UserProfile model (role field) | Dev | 1h | P1 |
| S1-05 | Build Login view + template | Dev | 1.5h | P1 |
| S1-06 | Build Registration view + template | Dev | 1.5h | P1 |
| S1-07 | Implement role-based access decorator | Dev | 1h | P1 |
| S1-08 | Build base HTML template (navbar, Bootstrap 5) | Dev | 1.5h | P1 |
| S1-09 | Create Admin user management page | Dev | 2h | P2 |
| S1-10 | Initial Git commit and repo setup | Dev | 0.5h | P1 |

**Sprint 1 Deliverable**: Login/Register working. Role-based redirects functional. Base layout complete.

---

## 3. Sprint 2 — Core Modules (Days 3–4)

**Goal**: Event CRUD, Resource Assignment, Budget Tracker

### Tasks

| Task ID | Task | Owner | Est. Hours | Priority |
|---|---|---|---|---|
| S2-01 | Create Event, Resource, EventResource models | Dev | 1.5h | P1 |
| S2-02 | Event list view with filters (category, status, date) | Dev | 2h | P1 |
| S2-03 | Event create/edit form (with all fields) | Dev | 2h | P1 |
| S2-04 | Event detail view | Dev | 1h | P1 |
| S2-05 | Event delete (with confirmation) | Dev | 0.5h | P1 |
| S2-06 | Resource management (add, list, assign to event) | Dev | 2h | P1 |
| S2-07 | Conflict warning when assigning already-booked resource | Dev | 1h | P2 |
| S2-08 | Create BudgetItem model | Dev | 0.5h | P1 |
| S2-09 | Budget tracker view (show estimated, spent, remaining) | Dev | 1.5h | P1 |
| S2-10 | Add expense form | Dev | 1h | P1 |
| S2-11 | Overspend alert (red highlight when actual > estimated) | Dev | 0.5h | P2 |

**Sprint 2 Deliverable**: Full event lifecycle working. Budget logging and summary functional.

---

## 4. Sprint 3 — Analytics & Risk (Days 5–6)

**Goal**: Dashboard, all 4 charts, risk log

### Tasks

| Task ID | Task | Owner | Est. Hours | Priority |
|---|---|---|---|---|
| S3-01 | Create Risk model | Dev | 0.5h | P1 |
| S3-02 | Risk log view (list all risks per event) | Dev | 1h | P1 |
| S3-03 | Add risk form with probability/impact selectors | Dev | 1h | P1 |
| S3-04 | Auto-calculate risk score on save | Dev | 0.5h | P1 |
| S3-05 | Risk status management (Open/Mitigated/Closed) | Dev | 0.5h | P2 |
| S3-06 | Dashboard summary cards (total events, budget, open risks) | Dev | 1.5h | P1 |
| S3-07 | Pie chart — event status distribution (Chart.js) | Dev | 1.5h | P1 |
| S3-08 | Bar chart — estimated vs. actual budget per event (Chart.js) | Dev | 1.5h | P1 |
| S3-09 | Line chart — events per month (Chart.js) | Dev | 1.5h | P1 |
| S3-10 | Risk Heatmap — 3×3 grid, color-coded (Chart.js bubble or custom HTML) | Dev | 2h | P1 |
| S3-11 | Analytics view with all charts on one page | Dev | 1h | P1 |

**Sprint 3 Deliverable**: Analytics dashboard complete with all 4 charts and risk heatmap. Risk log functional.

---

## 5. Sprint 4 — AI Features (Days 7–8)

**Goal**: Gemini API integration, smart scheduling, budget estimator

### Tasks

| Task ID | Task | Owner | Est. Hours | Priority |
|---|---|---|---|---|
| S4-01 | Install and configure `google-generativeai` SDK | Dev | 0.5h | P1 |
| S4-02 | Create `/ai/generate-description/` AJAX endpoint | Dev | 1.5h | P1 |
| S4-03 | Add "Generate Description" button to event create/edit form | Dev | 1h | P1 |
| S4-04 | Frontend JS: call AI endpoint on button click, fill textarea | Dev | 1h | P1 |
| S4-05 | Handle Gemini API errors gracefully (timeout, rate limit) | Dev | 0.5h | P1 |
| S4-06 | Smart scheduling logic (check venue availability, suggest 3 slots) | Dev | 2h | P1 |
| S4-07 | Create `/ai/suggest-slots/` AJAX endpoint | Dev | 1h | P1 |
| S4-08 | Display slot suggestions in event create form (clickable) | Dev | 1h | P2 |
| S4-09 | Budget estimator logic (average from past similar events) | Dev | 1.5h | P1 |
| S4-10 | Create `/ai/estimate-budget/` AJAX endpoint | Dev | 0.5h | P1 |
| S4-11 | Add "Estimate Budget" button to event create form | Dev | 0.5h | P1 |

**Sprint 4 Deliverable**: All AI features working. Description generation, smart scheduling, and budget estimator integrated into the event form.

---

## 6. Sprint 5 — Export, Testing & Polish (Days 9–10)

**Goal**: PDF export, complete testing, bug fixes, UI polish

### Tasks

| Task ID | Task | Owner | Est. Hours | Priority |
|---|---|---|---|---|
| S5-01 | Install WeasyPrint (or ReportLab as fallback) | Dev | 0.5h | P1 |
| S5-02 | Create event report PDF template (HTML) | Dev | 1.5h | P1 |
| S5-03 | Implement event PDF export view | Dev | 1h | P1 |
| S5-04 | Create analytics dashboard PDF export view | Dev | 1h | P2 |
| S5-05 | Test all user flows: Student, Faculty, Admin | Dev | 2h | P1 |
| S5-06 | Test all CRUD operations (events, budget, risks) | Dev | 1h | P1 |
| S5-07 | Test all AI endpoints (description, slots, budget) | Dev | 1h | P1 |
| S5-08 | Test PDF export for both event and dashboard | Dev | 0.5h | P1 |
| S5-09 | Fix identified bugs | Dev | 2h | P1 |
| S5-10 | UI polish: consistent spacing, colors, mobile responsiveness | Dev | 1h | P2 |
| S5-11 | Add seed data (sample events, budgets, risks) for demo | Dev | 0.5h | P2 |
| S5-12 | Final code review and documentation | Dev | 1h | P2 |

**Sprint 5 Deliverable**: Complete, tested, demo-ready application.

---

## 7. PERT/CPM — Critical Path

**Critical path** (longest path, cannot be delayed):

```
S1-01 → S1-03 → S1-04 → S1-05/06 → S2-01 → S2-02 → S2-08 → 
S3-01 → S3-06 → S3-07-10 → S4-02 → S4-06 → S5-01 → S5-05 → DONE
```

**Buffer activities** (can slip by 1 day without impact):
- User management page (S1-09)
- Conflict warning (S2-07)
- Risk status management (S3-05)
- Slot suggestion UI (S4-08)
- Analytics PDF (S5-04)

---

## 8. Definition of Done

A task is considered **Done** when:
- Feature is implemented and functional
- No console errors in browser
- Role restrictions are enforced
- Basic input validation is in place
- Tested manually with at least 2 user roles

---

## 9. Dependencies

| Dependency | Task Blocked | Notes |
|---|---|---|
| Gemini API key | S4-01 onwards | Required before AI sprint starts |
| WeasyPrint system deps | S5-01 | May need `libpango` installed on OS |
| Auth working | All feature tasks | Must be done in Sprint 1 |
| Event models done | Budget + Risk tasks | Sprint 2 before Sprint 3 |

---

## 10. Risk Register for Project Execution

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Gemini API quota exceeded | Low | High | Use caching; test with small prompts |
| WeasyPrint won't install on environment | Medium | Medium | Switch to ReportLab |
| AI features take longer than planned | Medium | High | Defer smart scheduling if needed; keep description generator |
| Timeline overrun | Medium | High | Cut UI polish; ensure core features (auth, CRUD, charts) are done first |

---

*Document Version 1.0 — CEMS Project Plan — Sterling & Partners*
