# Software Requirements Specification (SRS)
## College Event Management System (CEMS)

---

| Field | Details |
|---|---|
| **Document Type** | Software Requirements Specification |
| **Project** | College Event Management System |
| **Version** | 1.0 |
| **Date** | 2026-01-28 |
| **Prepared By** | Sterling & Partners |

---

## 1. Introduction

### 1.1 Purpose
This SRS defines all functional and non-functional requirements for the College Event Management System (CEMS). It serves as the reference document for the development team at Antigravity.

### 1.2 Intended Audience
- Antigravity development team
- Faculty advisors and evaluators
- Project stakeholders

### 1.3 Project Overview
CEMS is a Django-based web application that enables a college to plan, schedule, budget, and monitor events. It supports three user roles and integrates AI via the Gemini API for smart features.

---

## 2. Overall Description

### 2.1 Product Perspective
CEMS is a standalone web application. It does not integrate with existing ERP systems but is designed to be extensible. Data is stored in a relational database (SQLite for development, PostgreSQL for production).

### 2.2 User Classes

| User Class | Description | Access Level |
|---|---|---|
| **Student** | Can browse and view public events | Read-only on events |
| **Faculty Coordinator** | Can create, manage, and monitor their own events | CRUD on own events; read budget/risk |
| **Admin** | Full system access | Full CRUD; user management; all reports |

### 2.3 Operating Environment
- Web browser (Chrome, Firefox, Edge — latest versions)
- Python 3.10+
- Django 4.x
- SQLite (dev) / PostgreSQL (prod)

---

## 3. Functional Requirements

### FR-01: User Authentication

| ID | Requirement |
|---|---|
| FR-01.1 | The system shall allow users to register with email, password, and role selection |
| FR-01.2 | The system shall authenticate users via email and password |
| FR-01.3 | The system shall restrict views and actions based on user role |
| FR-01.4 | Admin shall be able to create, edit, and deactivate user accounts |
| FR-01.5 | The system shall support secure logout |
| FR-01.6 | Unauthenticated users shall only see the login/register page |

---

### FR-02: Event Management

| ID | Requirement |
|---|---|
| FR-02.1 | Faculty/Admin shall be able to create an event with: name, description, category, date, time, venue, organizer, expected attendees |
| FR-02.2 | The system shall provide an AI-powered "Generate Description" button on the event creation form |
| FR-02.3 | Clicking the generate button shall call the Gemini API with the event name and return a description |
| FR-02.4 | Faculty/Admin shall be able to edit event details |
| FR-02.5 | Admin shall be able to delete any event; Faculty can delete only their own |
| FR-02.6 | Events shall have a status field: Planned / In Progress / Completed / Cancelled |
| FR-02.7 | Students shall be able to view a list of all events with filters (by date, category, status) |
| FR-02.8 | Each event shall support attaching resources (venue, equipment) and volunteers |

---

### FR-03: Resource Assignment

| ID | Requirement |
|---|---|
| FR-03.1 | Admin/Faculty shall be able to add resources (name, type: venue/equipment, capacity) |
| FR-03.2 | Resources shall be assignable to events |
| FR-03.3 | The system shall warn if a resource is already booked for the same date/time |

---

### FR-04: Budget Tracker

| ID | Requirement |
|---|---|
| FR-04.1 | Each event shall have an estimated budget set at creation |
| FR-04.2 | Faculty/Admin shall be able to log expense items (category, description, amount, date) |
| FR-04.3 | The system shall calculate and display remaining budget in real time |
| FR-04.4 | The system shall visually highlight overspent events (red indicator) |
| FR-04.5 | Budget summary (estimated, spent, remaining) shall be visible on the event detail page |

---

### FR-05: Risk Log

| ID | Requirement |
|---|---|
| FR-05.1 | Faculty/Admin shall be able to add risks per event: title, description, probability (Low/Medium/High), impact (Low/Medium/High) |
| FR-05.2 | The system shall auto-calculate risk score as Probability × Impact (1–9 scale) |
| FR-05.3 | Each risk shall have a mitigation plan field |
| FR-05.4 | Risk status shall be: Open / Mitigated / Closed |
| FR-05.5 | Admin shall see all risks across all events |

---

### FR-06: Dashboard

| ID | Requirement |
|---|---|
| FR-06.1 | Dashboard shall display summary cards: Total Events, Upcoming Events, Total Budget Used, Open Risks |
| FR-06.2 | Dashboard shall show a list of recent events |
| FR-06.3 | Dashboard shall show flagged risks (High score risks highlighted) |
| FR-06.4 | Admin dashboard shall show system-wide data; Faculty sees only their events |

---

### FR-07: Analytics & Charts

| ID | Requirement |
|---|---|
| FR-07.1 | The system shall display a **Pie Chart** of event status distribution |
| FR-07.2 | The system shall display a **Bar Chart** of estimated vs. actual budget per event |
| FR-07.3 | The system shall display a **Line Chart** of number of events per month |
| FR-07.4 | The system shall display a **Risk Heatmap** (3×3 grid: Probability vs. Impact, color-coded green/yellow/red) |
| FR-07.5 | All charts shall be rendered using Chart.js |

---

### FR-08: AI — Smart Scheduling

| ID | Requirement |
|---|---|
| FR-08.1 | When creating an event, if the user selects a venue, the system shall check existing bookings |
| FR-08.2 | The system shall suggest 3 available conflict-free time slots for the selected venue and date range |
| FR-08.3 | Suggestions shall be displayed inline on the event creation form |

---

### FR-09: AI — Budget Estimator

| ID | Requirement |
|---|---|
| FR-09.1 | On the event creation form, the system shall provide a "Estimate Budget" button |
| FR-09.2 | On click, the system shall look up past events of the same category and compute the average cost |
| FR-09.3 | The estimate shall be pre-filled in the estimated budget field (editable) |
| FR-09.4 | If no historical data exists, the system shall display a default range suggestion |

---

### FR-10: PDF Export

| ID | Requirement |
|---|---|
| FR-10.1 | Admin/Faculty shall be able to export a single event's full report as PDF |
| FR-10.2 | The PDF report shall include: event details, budget summary, expense list, risk log |
| FR-10.3 | Admin shall be able to export the analytics dashboard as PDF |
| FR-10.4 | PDF generation shall use WeasyPrint or ReportLab |

---

## 4. Non-Functional Requirements

### 4.1 Performance
- Page load time shall be under 3 seconds for all core views
- API calls to Gemini shall complete within 10 seconds; a loading indicator shall be shown

### 4.2 Security
- Passwords shall be hashed using Django's default PBKDF2 algorithm
- CSRF protection shall be enabled on all forms
- Role checks shall be enforced server-side (not just frontend)
- Sensitive API keys (Gemini) shall be stored in environment variables, not in source code

### 4.3 Usability
- UI shall be responsive and mobile-friendly (Bootstrap 5)
- All forms shall have validation with user-friendly error messages
- Success/error flash messages shall be shown after all major actions

### 4.4 Reliability
- The system shall gracefully handle Gemini API failures (show error message, allow manual input)
- The system shall validate all user inputs server-side

### 4.5 Maintainability
- Code shall follow PEP 8 style guidelines
- Each Django app shall have a single responsibility (events, budget, risks, analytics)
- All secret keys and config shall use `django-environ` or `.env` files

---

## 5. External Interface Requirements

### 5.1 Gemini API
- **Endpoint**: Google Generative AI SDK (`google-generativeai` Python package)
- **Trigger**: Event description generation button
- **Input**: Event name (string)
- **Output**: Generated description text (string)
- **Error Handling**: Timeout after 10 seconds; display "Generation failed, please type manually"

### 5.2 Chart.js
- **Source**: CDN (`https://cdn.jsdelivr.net/npm/chart.js`)
- **Usage**: Client-side rendering of all 4 charts
- **Data**: Passed from Django views as JSON in template context

### 5.3 PDF Generator (WeasyPrint / ReportLab)
- **Trigger**: "Export PDF" button on event detail or analytics pages
- **Output**: Downloadable `.pdf` file

---

## 6. Use Case Summary

| Use Case | Actor | Description |
|---|---|---|
| UC-01 | All Users | Login to the system |
| UC-02 | Admin | Create and manage user accounts |
| UC-03 | Faculty/Admin | Create, edit, delete events |
| UC-04 | Faculty/Admin | Generate event description via AI |
| UC-05 | Faculty/Admin | Assign resources to events |
| UC-06 | Faculty/Admin | Log and track budget expenses |
| UC-07 | Faculty/Admin | Add and manage risks |
| UC-08 | Faculty/Admin | View smart scheduling suggestions |
| UC-09 | Faculty/Admin | Use budget estimator |
| UC-10 | Admin/Faculty | View analytics dashboard and charts |
| UC-11 | Admin/Faculty | Export event or dashboard PDF |
| UC-12 | Student | Browse and filter events |

---

## 7. Acceptance Criteria

| Feature | Acceptance Criteria |
|---|---|
| Auth | Users can register, login, and are restricted by role |
| Event CRUD | All CRUD operations work; AI description generates on click |
| Budget Tracker | Expenses logged; remaining budget calculated correctly |
| Risk Log | Risks created with auto-calculated score; heatmap shows correct placement |
| Dashboard | Summary cards show correct counts; charts render with real data |
| Smart Scheduling | At least 3 conflict-free slots suggested per venue/date |
| Budget Estimator | Returns average from historical data or default range |
| PDF Export | Clean, readable PDF downloaded on button click |

---

*Document Version 1.0 — CEMS SRS — Sterling & Partners*
