# API & Endpoint Reference
## College Event Management System (CEMS)

---

| Field | Details |
|---|---|
| **Document Type** | API & Endpoint Reference |
| **Project** | College Event Management System |
| **Version** | 1.0 |
| **Date** | 2026-01-28 |

---

> Note: CEMS uses Django's server-rendered views (not a REST API). However, three AJAX endpoints exist for AI features. All regular pages return HTML. This document covers both page routes and AJAX endpoints.

---

## 1. Authentication Endpoints

| Method | URL | View | Auth Required | Description |
|---|---|---|---|---|
| GET/POST | `/accounts/login/` | `login_view` | No | Login page |
| GET | `/accounts/logout/` | `logout_view` | Yes | Logout |
| GET/POST | `/accounts/register/` | `register_view` | No | Registration page |
| GET/POST | `/accounts/users/` | `user_list` | Admin only | List/manage users |
| GET/POST | `/accounts/users/<id>/edit/` | `user_edit` | Admin only | Edit user role |

---

## 2. Event Endpoints

| Method | URL | View | Auth Required | Description |
|---|---|---|---|---|
| GET | `/events/` | `event_list` | Yes | List all events (filterable) |
| GET/POST | `/events/create/` | `event_create` | Faculty/Admin | Create new event |
| GET | `/events/<id>/` | `event_detail` | Yes | View event details |
| GET/POST | `/events/<id>/edit/` | `event_edit` | Faculty/Admin | Edit event |
| POST | `/events/<id>/delete/` | `event_delete` | Faculty/Admin | Delete event |
| POST | `/events/<id>/status/` | `event_status_update` | Faculty/Admin | Update event status |

**Query Params for `/events/`:**
- `?category=technical` — filter by category
- `?status=planned` — filter by status
- `?date=2026-03` — filter by month

---

## 3. Resource Endpoints

| Method | URL | View | Auth Required | Description |
|---|---|---|---|---|
| GET | `/resources/` | `resource_list` | Faculty/Admin | List all resources |
| GET/POST | `/resources/create/` | `resource_create` | Admin | Add new resource |
| POST | `/events/<id>/resources/assign/` | `assign_resource` | Faculty/Admin | Assign resource to event |
| POST | `/events/<id>/resources/<rid>/remove/` | `remove_resource` | Faculty/Admin | Remove resource from event |

---

## 4. Budget Endpoints

| Method | URL | View | Auth Required | Description |
|---|---|---|---|---|
| GET | `/events/<id>/budget/` | `budget_detail` | Faculty/Admin | View budget tracker |
| GET/POST | `/events/<id>/budget/add/` | `add_expense` | Faculty/Admin | Add expense item |
| POST | `/events/<id>/budget/<eid>/delete/` | `delete_expense` | Faculty/Admin | Delete expense item |

---

## 5. Risk Endpoints

| Method | URL | View | Auth Required | Description |
|---|---|---|---|---|
| GET | `/events/<id>/risks/` | `risk_list` | Faculty/Admin | View all risks for event |
| GET/POST | `/events/<id>/risks/add/` | `add_risk` | Faculty/Admin | Add new risk |
| GET/POST | `/events/<id>/risks/<rid>/edit/` | `edit_risk` | Faculty/Admin | Edit risk |
| POST | `/events/<id>/risks/<rid>/delete/` | `delete_risk` | Faculty/Admin | Delete risk |

---

## 6. Analytics Endpoints

| Method | URL | View | Auth Required | Description |
|---|---|---|---|---|
| GET | `/analytics/` | `analytics_dashboard` | Faculty/Admin | Analytics dashboard with all charts |
| GET | `/analytics/export-pdf/` | `export_analytics_pdf` | Admin | Download analytics PDF |
| GET | `/events/<id>/export-pdf/` | `export_event_pdf` | Faculty/Admin | Download event report PDF |

---

## 7. AI Feature AJAX Endpoints

These endpoints are called via JavaScript `fetch()` from the browser. They return JSON.

---

### 7.1 Generate Event Description

**POST** `/ai/generate-description/`

**Request:**
```json
{
  "event_name": "Tech Fest 2026"
}
```

**Response (200 OK):**
```json
{
  "description": "Tech Fest 2026 is an exciting annual celebration of innovation and technology, designed for engineering students and tech enthusiasts. Attendees can look forward to competitions, workshops, and keynote sessions from industry leaders. Whether you're a coder, designer, or simply curious about the future of tech, this event has something for everyone."
}
```

**Response (500 Error):**
```json
{
  "error": "Gemini API request failed. Please type your description manually."
}
```

**Auth**: Login required

---

### 7.2 Smart Scheduling — Suggest Slots

**POST** `/ai/suggest-slots/`

**Request:**
```json
{
  "venue_id": 1,
  "preferred_date": "2026-03-15"
}
```

**Response (200 OK):**
```json
{
  "slots": [
    { "start": "2026-03-15T09:00:00", "end": "2026-03-15T11:00:00" },
    { "start": "2026-03-15T13:00:00", "end": "2026-03-15T15:00:00" },
    { "start": "2026-03-15T16:00:00", "end": "2026-03-15T18:00:00" }
  ]
}
```

**Response (no slots available):**
```json
{
  "slots": [],
  "message": "No available slots found for this venue on the selected date."
}
```

**Auth**: Faculty/Admin required

---

### 7.3 Budget Estimator

**POST** `/ai/estimate-budget/`

**Request:**
```json
{
  "category": "technical",
  "expected_attendees": 200
}
```

**Response (200 OK — from historical data):**
```json
{
  "estimate": 27500.00,
  "based_on": 5,
  "is_default": false,
  "message": "Based on average of 5 similar past events."
}
```

**Response (200 OK — default fallback):**
```json
{
  "estimate": 25000.00,
  "is_default": true,
  "message": "No historical data available. This is a suggested default for technical events."
}
```

**Auth**: Faculty/Admin required

---

## 8. Chart Data Format Reference

Chart data is passed to templates as JSON. Reference for frontend developers:

### 8.1 Pie Chart (Event Status)
```json
[
  { "status": "planned", "count": 5 },
  { "status": "in_progress", "count": 3 },
  { "status": "completed", "count": 10 },
  { "status": "cancelled", "count": 1 }
]
```

### 8.2 Bar Chart (Budget)
```json
[
  { "name": "Tech Fest 2026", "estimated_budget": 30000, "actual": 27500 },
  { "name": "Cultural Day", "estimated_budget": 50000, "actual": 52000 }
]
```

### 8.3 Line Chart (Monthly Frequency)
```json
[
  { "month": "2026-01", "count": 2 },
  { "month": "2026-02", "count": 4 },
  { "month": "2026-03", "count": 7 }
]
```

### 8.4 Risk Heatmap Data
```json
[
  { "probability": 3, "impact": 3, "count": 2, "label": "Critical" },
  { "probability": 2, "impact": 3, "count": 1, "label": "High" },
  { "probability": 1, "impact": 1, "count": 4, "label": "Low" }
]
```

---

*Document Version 1.0 — CEMS API Reference — Sterling & Partners*
