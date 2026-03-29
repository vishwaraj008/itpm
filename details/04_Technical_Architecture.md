# Technical Architecture Document (TAD)
## College Event Management System (CEMS)

---

| Field | Details |
|---|---|
| **Document Type** | Technical Architecture Document |
| **Project** | College Event Management System |
| **Version** | 1.0 |
| **Date** | 2026-01-28 |

---

## 1. Architecture Overview

CEMS follows a **monolithic MVC architecture** using Django's MVT (Model-View-Template) pattern. The frontend is server-rendered HTML via Django templates with Chart.js for client-side charts. The Gemini AI API is called server-side from Django views.

---

## 2. Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT (Browser)                   │
│  Bootstrap 5 UI │ Chart.js │ Fetch API (AI triggers)    │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTP / HTTPS
┌──────────────────────────▼──────────────────────────────┐
│                   DJANGO WEB SERVER                     │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  accounts/  │  │   events/    │  │   budget/     │  │
│  │  (auth,     │  │  (CRUD,      │  │  (expenses,   │  │
│  │   roles)    │  │   resources) │  │   tracking)   │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   risks/    │  │  analytics/  │  │  ai_features/ │  │
│  │  (risk log, │  │  (charts,    │  │  (Gemini API, │  │
│  │   heatmap)  │  │   PDF)       │  │   scheduler)  │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                                                         │
└──────────────┬────────────────────────┬────────────────┘
               │                        │
┌──────────────▼──────────┐   ┌─────────▼────────────────┐
│    SQLite / PostgreSQL  │   │      Gemini API           │
│    (ORM via Django)     │   │  (google-generativeai)    │
└─────────────────────────┘   └──────────────────────────┘
```

---

## 3. Technology Stack Details

### 3.1 Backend

| Component | Choice | Reason |
|---|---|---|
| Language | Python 3.10+ | Team familiarity, rich ecosystem |
| Framework | Django 4.x | Built-in auth, ORM, admin, forms |
| ORM | Django ORM | Simplifies DB queries; no raw SQL needed |
| API Handling | Django Views (function-based) | Simple; sufficient for project scale |

### 3.2 Frontend

| Component | Choice | Reason |
|---|---|---|
| Templates | Django Templates | Tight integration with backend data |
| CSS Framework | Bootstrap 5 | Responsive, fast to implement |
| Charts | Chart.js | Easy to use, CDN-available, supports all required chart types |
| Icons | Bootstrap Icons | Free, consistent, CDN-available |

### 3.3 AI Integration

| Component | Choice | Reason |
|---|---|---|
| AI Provider | Google Gemini API | Free tier, capable, Python SDK available |
| SDK | `google-generativeai` | Official Python package |
| Model | `gemini-1.5-flash` | Fast responses; free tier compatible |

**Integration Flow:**
```
User clicks "Generate Description"
        ↓
Frontend sends AJAX POST request to /ai/generate-description/
        ↓
Django view receives event_name
        ↓
Calls Gemini API: model.generate_content(prompt)
        ↓
Returns JSON { "description": "..." }
        ↓
Frontend fills textarea with result
```

### 3.4 PDF Generation

| Library | Usage | Notes |
|---|---|---|
| `WeasyPrint` | Preferred — renders HTML templates to PDF | Requires system dependencies (libpango) |
| `ReportLab` | Fallback — programmatic PDF creation | Pure Python, no system deps |

**Recommendation**: Try WeasyPrint first. If deployment environment doesn't support it, use ReportLab.

### 3.5 Database

| Environment | Database | Notes |
|---|---|---|
| Development | SQLite | Zero setup, file-based |
| Production | PostgreSQL | Concurrent users, better performance |

---

## 4. URL Structure

```
/                          → Redirect to dashboard if logged in, else login
/accounts/login/           → Login page
/accounts/logout/          → Logout
/accounts/register/        → Registration
/accounts/users/           → User management (Admin only)

/dashboard/                → Main dashboard

/events/                   → Event list
/events/create/            → Create event form
/events/<id>/              → Event detail
/events/<id>/edit/         → Edit event
/events/<id>/delete/       → Delete event

/events/<id>/budget/       → Budget tracker for event
/events/<id>/budget/add/   → Add expense

/events/<id>/risks/        → Risk log for event
/events/<id>/risks/add/    → Add risk

/analytics/                → Analytics dashboard (charts)
/analytics/export-pdf/     → Export analytics as PDF
/events/<id>/export-pdf/   → Export event report as PDF

/ai/generate-description/  → AJAX endpoint: Gemini description generator
/ai/suggest-slots/         → AJAX endpoint: Smart scheduling
/ai/estimate-budget/       → AJAX endpoint: Budget estimator
```

---

## 5. Security Design

| Concern | Implementation |
|---|---|
| Authentication | Django's built-in `@login_required` decorator |
| Role Authorization | Custom `@role_required(role)` decorator checking `user.userprofile.role` |
| CSRF Protection | Django CSRF middleware (enabled by default) |
| Password Hashing | PBKDF2 with SHA256 (Django default) |
| API Key Storage | Stored in `.env` file; loaded via `django-environ`; never committed to Git |
| SQL Injection | Protected by Django ORM parameterized queries |
| XSS | Django templates auto-escape HTML by default |

---

## 6. AI Feature Implementation Details

### 6.1 Event Description Generator

```python
# ai_features/views.py
import google.generativeai as genai
from django.http import JsonResponse
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_description(request):
    if request.method == "POST":
        event_name = request.POST.get("event_name", "")
        prompt = f"""
        Write a professional and engaging event description for a college event named "{event_name}".
        Keep it to 3-4 sentences. Mention the purpose, target audience, and what attendees can expect.
        """
        try:
            response = model.generate_content(prompt)
            return JsonResponse({"description": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
```

### 6.2 Smart Scheduling

```python
# Logic: Given venue and preferred date, find 3 free slots

def suggest_slots(request):
    venue_id = request.POST.get("venue_id")
    preferred_date = request.POST.get("date")  # YYYY-MM-DD
    
    # Get all bookings for this venue on this date
    booked = Event.objects.filter(
        venue_id=venue_id,
        start_datetime__date=preferred_date
    ).values("start_datetime", "end_datetime")
    
    # Generate candidate slots (e.g., 9am–6pm, 2-hour blocks)
    # Return first 3 that don't overlap with booked
    # Return as JSON list of {"start": "...", "end": "..."}
```

### 6.3 Budget Estimator

```python
# Logic: Average estimated_budget of past events with same category

def estimate_budget(request):
    category = request.POST.get("category")
    past_events = Event.objects.filter(
        category=category,
        status="completed",
        estimated_budget__gt=0
    )
    if past_events.exists():
        avg = past_events.aggregate(Avg("estimated_budget"))["estimated_budget__avg"]
        return JsonResponse({"estimate": round(avg, 2)})
    else:
        # Default ranges per category
        defaults = {
            "technical": 25000,
            "cultural": 40000,
            "academic": 15000,
            "sports": 20000,
            "other": 10000
        }
        return JsonResponse({"estimate": defaults.get(category, 10000), "is_default": True})
```

---

## 7. Chart.js Data Flow

All chart data is prepared in Django views and passed to templates as JSON:

```python
# analytics/views.py
def analytics_dashboard(request):
    # Pie chart: event status
    status_data = Event.objects.values("status").annotate(count=Count("id"))
    
    # Bar chart: budget per event
    budget_data = Event.objects.annotate(
        actual=Sum("budgetitem__amount")
    ).values("name", "estimated_budget", "actual")
    
    # Line chart: events per month
    monthly_data = Event.objects.annotate(
        month=TruncMonth("start_datetime")
    ).values("month").annotate(count=Count("id")).order_by("month")
    
    return render(request, "analytics/dashboard.html", {
        "status_data": json.dumps(list(status_data)),
        "budget_data": json.dumps(list(budget_data)),
        "monthly_data": json.dumps(list(monthly_data)),
    })
```

---

## 8. PDF Export Flow

```
User clicks "Export PDF"
        ↓
Django view renders HTML template with event data
        ↓
WeasyPrint converts HTML → PDF bytes
        ↓
Django returns HttpResponse with content_type="application/pdf"
        ↓
Browser prompts user to download
```

---

## 9. Environment Configuration

**.env file (never commit to Git)**

```
SECRET_KEY=your-django-secret-key
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

**settings.py**

```python
import environ
env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env("SECRET_KEY")
GEMINI_API_KEY = env("GEMINI_API_KEY")
```

---

## 10. Required Python Packages

```txt
# requirements.txt
Django>=4.2
google-generativeai>=0.4.0
django-environ>=0.11.0
WeasyPrint>=60.0
Pillow>=10.0.0
django-crispy-forms>=2.0
crispy-bootstrap5>=0.7
```

---

*Document Version 1.0 — CEMS Technical Architecture — Sterling & Partners*
