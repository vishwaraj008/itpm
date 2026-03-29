# Database Design Document (DDD)
## College Event Management System (CEMS)

---

| Field | Details |
|---|---|
| **Document Type** | Database Design Document |
| **Project** | College Event Management System |
| **Version** | 1.0 |
| **Date** | 2026-01-28 |

---

## 1. Overview

CEMS uses a relational database. SQLite is used during development; PostgreSQL is recommended for production. All models are defined as Django ORM models.

---

## 2. Entity Relationship Overview

```
User ──< Event (organizer)
Event ──< EventResource
Resource ──< EventResource
Event ──< BudgetItem
Event ──< Risk
```

---

## 3. Database Tables / Django Models

### 3.1 User (Extended Django Auth User)

**Table: `auth_user` + `userprofile`**

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PK, Auto | User ID |
| `username` | Varchar(150) | Unique, Not Null | Login username |
| `email` | Varchar(254) | Unique, Not Null | Email address |
| `password` | Varchar(128) | Not Null | Hashed password |
| `first_name` | Varchar(150) | | First name |
| `last_name` | Varchar(150) | | Last name |
| `is_active` | Boolean | Default: True | Account active status |
| `date_joined` | DateTime | Auto | Registration date |

**UserProfile (One-to-One with User)**

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PK, Auto | Profile ID |
| `user` | FK → User | One-to-One | Linked user |
| `role` | Varchar(20) | Choices: student/faculty/admin | User role |
| `department` | Varchar(100) | Nullable | Department/class |
| `phone` | Varchar(15) | Nullable | Contact number |

---

### 3.2 Event

**Table: `events_event`**

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PK, Auto | Event ID |
| `name` | Varchar(200) | Not Null | Event name |
| `description` | TextField | Nullable | Event description (AI-generated or manual) |
| `category` | Varchar(50) | Choices: academic/cultural/technical/sports/other | Event type |
| `start_datetime` | DateTime | Not Null | Event start date and time |
| `end_datetime` | DateTime | Not Null | Event end date and time |
| `venue` | FK → Resource | Nullable, on_delete=SET_NULL | Venue assigned |
| `organizer` | FK → User | Not Null, on_delete=CASCADE | Faculty/Admin who created it |
| `expected_attendees` | Integer | Default: 0 | Expected headcount |
| `estimated_budget` | Decimal(10,2) | Default: 0.00 | Estimated budget (INR) |
| `status` | Varchar(20) | Choices: planned/in_progress/completed/cancelled | Current status |
| `created_at` | DateTime | Auto | Creation timestamp |
| `updated_at` | DateTime | Auto | Last update timestamp |

---

### 3.3 Resource

**Table: `events_resource`**

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PK, Auto | Resource ID |
| `name` | Varchar(150) | Not Null | Resource name (e.g., "Auditorium A") |
| `resource_type` | Varchar(20) | Choices: venue/equipment/other | Type of resource |
| `capacity` | Integer | Nullable | Max capacity (for venues) |
| `description` | TextField | Nullable | Additional details |
| `is_available` | Boolean | Default: True | General availability flag |

---

### 3.4 EventResource (Many-to-Many junction)

**Table: `events_eventresource`**

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PK, Auto | Record ID |
| `event` | FK → Event | Not Null, on_delete=CASCADE | Associated event |
| `resource` | FK → Resource | Not Null, on_delete=CASCADE | Assigned resource |
| `notes` | TextField | Nullable | Notes on usage |

---

### 3.5 BudgetItem

**Table: `budget_budgetitem`**

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PK, Auto | Expense ID |
| `event` | FK → Event | Not Null, on_delete=CASCADE | Associated event |
| `category` | Varchar(50) | Choices: catering/decoration/logistics/marketing/technology/other | Expense category |
| `description` | Varchar(255) | Not Null | Expense description |
| `amount` | Decimal(10,2) | Not Null | Amount spent (INR) |
| `date` | Date | Not Null | Date of expense |
| `added_by` | FK → User | Not Null, on_delete=CASCADE | Who logged it |
| `created_at` | DateTime | Auto | Creation timestamp |

---

### 3.6 Risk

**Table: `risks_risk`**

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PK, Auto | Risk ID |
| `event` | FK → Event | Not Null, on_delete=CASCADE | Associated event |
| `title` | Varchar(200) | Not Null | Risk title |
| `description` | TextField | Not Null | Detailed description |
| `probability` | Integer | Choices: 1 (Low) / 2 (Medium) / 3 (High) | Likelihood |
| `impact` | Integer | Choices: 1 (Low) / 2 (Medium) / 3 (High) | Severity |
| `risk_score` | Integer | Auto-calculated: probability × impact | Score (1–9) |
| `mitigation_plan` | TextField | Nullable | How to address the risk |
| `status` | Varchar(20) | Choices: open/mitigated/closed | Current status |
| `identified_by` | FK → User | Not Null | Who added the risk |
| `created_at` | DateTime | Auto | Creation timestamp |

---

## 4. Django App Structure

```
cems/
├── cems/                    # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # User auth + profiles
│   ├── models.py            # UserProfile
│   ├── views.py
│   └── urls.py
├── events/                  # Event CRUD + resources
│   ├── models.py            # Event, Resource, EventResource
│   ├── views.py
│   └── urls.py
├── budget/                  # Budget tracking
│   ├── models.py            # BudgetItem
│   ├── views.py
│   └── urls.py
├── risks/                   # Risk log
│   ├── models.py            # Risk
│   ├── views.py
│   └── urls.py
├── analytics/               # Charts + PDF export
│   ├── views.py             # Chart data endpoints + PDF
│   └── urls.py
├── ai_features/             # Gemini API + smart features
│   ├── views.py             # Description gen, scheduler, estimator
│   └── urls.py
└── templates/               # HTML templates
    ├── base.html
    ├── dashboard.html
    ├── events/
    ├── budget/
    ├── risks/
    └── analytics/
```

---

## 5. Key Relationships Summary

| Relationship | Type | Description |
|---|---|---|
| User → UserProfile | One-to-One | Each user has one profile with role |
| User → Event (organizer) | One-to-Many | One user organizes many events |
| Event → Resource (venue) | Many-to-One | One event has one venue |
| Event ↔ Resource (via EventResource) | Many-to-Many | Events can have multiple equipment/resources |
| Event → BudgetItem | One-to-Many | One event has many expense entries |
| Event → Risk | One-to-Many | One event has many risks |

---

## 6. Sample Data / Seed Data

For development and testing, seed the following:

**Users**
- `admin@cems.com` / Role: Admin
- `faculty1@cems.com` / Role: Faculty Coordinator
- `student1@cems.com` / Role: Student

**Resources**
- Auditorium A (venue, capacity: 500)
- Seminar Hall B (venue, capacity: 100)
- Projector Set 1 (equipment)
- Sound System (equipment)

**Events**
- Tech Fest 2026 (Technical, Feb 15)
- Annual Cultural Day (Cultural, Mar 10)
- Science Exhibition (Academic, Apr 5)

---

*Document Version 1.0 — CEMS Database Design — Sterling & Partners*
