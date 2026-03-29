# Project Design Report (PDR)
## College Event Management System (CEMS)

---

| Field              | Details                            |
|--------------------|------------------------------------|
| **Project Title**  | College Event Management System    |
| **Client**         | Antigravity                        |
| **Prepared By**    | Sterling & Partners                |
| **Date**           | 2026-01-28                         |
| **Version**        | 1.0                                |
| **Classification** | Internal / Project Documentation   |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Project Objectives](#3-project-objectives)
4. [Project Scope](#4-project-scope)
5. [Proposed Solution](#5-proposed-solution)
6. [System Architecture](#6-system-architecture)
7. [Feature Breakdown](#7-feature-breakdown)
8. [Technology Stack](#8-technology-stack)
9. [Project Methodology](#9-project-methodology)
10. [Risk Analysis](#10-risk-analysis)
11. [Cost Estimation](#11-cost-estimation)
12. [Timeline & Milestones](#12-timeline--milestones)
13. [Expected Outcomes](#13-expected-outcomes)
14. [Assumptions & Constraints](#14-assumptions--constraints)
15. [Sign-Off](#15-sign-off)

---

## 1. Executive Summary

The College Event Management System (CEMS) is a web-based platform designed to streamline the planning, scheduling, budgeting, and monitoring of academic and cultural events within a college environment. Currently, event coordination is handled manually through emails, spreadsheets, and meetings — leading to schedule conflicts, budget mismanagement, poor resource coordination, and limited project tracking.

CEMS addresses these pain points by providing a centralized, role-aware platform for Students, Faculty Coordinators, and Administrators. The system incorporates traditional project management techniques (WBS, PERT/CPM, risk analysis) alongside modern tools (AI-powered event description generation, analytics dashboards, and smart scheduling suggestions).

This document outlines the full design, architecture, feature set, methodology, risk assessment, and project plan for the CEMS to be built by Antigravity within a 10-day development sprint.

---

## 2. Problem Statement

Colleges organize multiple academic, cultural, and technical events each year. The current manual process suffers from:

| # | Problem | Impact |
|---|---------|--------|
| 01 | Schedule conflicts between events | Double bookings, poor attendance |
| 02 | Budget mismanagement | Overspending, no real-time tracking |
| 03 | Poor resource coordination | Wasted resources, last-minute scrambles |
| 04 | Limited project tracking | No visibility into event progress |

A structured, digital project management approach is required to manage IT-based event operations efficiently.

---

## 3. Project Objectives

The primary goals of CEMS are:

1. Provide role-based access for Students, Faculty Coordinators, and Administrators
2. Enable full event lifecycle management (create → schedule → execute → close)
3. Track and control budgets in real time
4. Log and manage risks associated with each event
5. Offer data-driven analytics and visual reporting
6. Integrate AI to assist with event descriptions and smart scheduling
7. Support PDF report exports for administrative use

---

## 4. Project Scope

### 4.1 In Scope

| Feature Area | Details |
|---|---|
| Authentication | Login, logout, role-based access (Student / Faculty / Admin) |
| Event Management | Create, read, update, delete events with scheduling |
| Resource Assignment | Assign venues, equipment, volunteers to events |
| Budget Tracker | Estimated vs. actual cost tracking per event |
| Risk Log | Risk identification, classification, mitigation |
| Dashboard | Overview of all events, KPIs, status |
| Analytics | Pie chart (event status), bar chart (budget), line chart (monthly frequency), risk heatmap |
| AI Feature | Gemini API — auto-generate event descriptions |
| Smart Scheduling | Conflict-free time slot suggestions based on existing bookings |
| Budget Estimator | Predict event costs based on historical event data |
| PDF Export | Export event reports and dashboards as PDF |

### 4.2 Out of Scope

| Excluded Feature | Reason |
|---|---|
| Advanced UI/UX animations | Timeline constraint |
| Payment gateway integration | Out of academic scope |
| Large-scale production deployment | Not required for PBL case study |
| Mobile application | Web-first for current phase |
| Multi-college / multi-tenant support | Future phase |

---

## 5. Proposed Solution

CEMS will be built as a **Django-based web application** with a relational database backend. The system will have a clean, responsive UI using Bootstrap, integrated with Chart.js for analytics visualization and the Gemini API for AI-powered content generation.

The solution follows a **hybrid project management methodology**:
- **Traditional PM**: Feasibility, WBS, PERT/CPM scheduling, cost estimation
- **Agile Scrum**: 2-day sprints, sprint planning, iterative delivery
- **DevOps**: Version control via Git, structured deployment pipeline

---

## 6. System Architecture

```
┌──────────────────────────────────────────────────┐
│                   STAKEHOLDERS                   │
│     Students   │  Faculty Coordinators  │  Admin │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│              USER INTERFACE LAYER                │
│           Django Templates + Bootstrap           │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│              APPLICATION LAYER                   │
│  Event Planning │ Scheduling │ Budget │ Resources │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│           PROJECT MANAGEMENT LAYER               │
│  WBS │ Cost Estimation │ Risk Analysis │ Sprints  │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│              AI & ANALYTICS LAYER                │
│  Gemini API │ Smart Scheduler │ Budget Estimator  │
│  Chart.js Dashboard │ Risk Heatmap               │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│                 DATABASE LAYER                   │
│       SQLite (dev) / PostgreSQL (prod)           │
│  Event Data │ Cost Data │ User Data │ Risk Data  │
└──────────────────────────────────────────────────┘
```

---

## 7. Feature Breakdown

### 7.1 Authentication & Role Management
- Login / Logout with Django's built-in auth system
- Three roles: **Student**, **Faculty Coordinator**, **Admin**
- Role-based view restrictions via decorators / middleware
- Admin can manage users and assign roles

### 7.2 Event Management (CRUD)
- Create events with: name, description, category, date/time, venue, organizer
- AI-powered description generator (Gemini API) triggered by event name
- Edit and delete events (Faculty/Admin only)
- Student view: browse and filter events
- Assign resources (rooms, equipment) and volunteers per event
- Status tracking: Planned → In Progress → Completed → Cancelled

### 7.3 Budget Tracker
- Set estimated budget per event at creation
- Log actual expenditure line items (category, amount, date)
- Real-time remaining budget calculation
- Overspend alerts (highlighted in red on dashboard)

### 7.4 Risk Log
- Log risks per event: title, description, probability (Low/Med/High), impact (Low/Med/High)
- Auto-calculate Risk Score = Probability × Impact
- Mitigation plan field
- Risk status: Open / Mitigated / Closed

### 7.5 Dashboard
- Summary cards: Total Events, Upcoming Events, Total Budget Used, Risks Open
- Quick links to recent events and flagged risks
- Role-specific view (Admin sees everything; Faculty sees their events; Students see public events)

### 7.6 Analytics & Charts
- **Pie Chart**: Event status distribution (Planned / In Progress / Completed / Cancelled)
- **Bar Chart**: Budget estimated vs. actual per event
- **Line Chart**: Number of events per month (frequency trend)
- **Risk Heatmap**: 3×3 grid — Probability (Y-axis) vs. Impact (X-axis), color-coded (green → red)

### 7.7 AI Features
- **Event Description Generator**: User types event name → clicks "Generate" → Gemini API returns a professional event description
- **Smart Scheduling**: When creating an event, system checks existing bookings for the venue and suggests 3 conflict-free time slots
- **Budget Estimator**: Based on event category and expected attendee count, estimates budget using average of past similar events stored in DB

### 7.8 PDF Export
- Export individual event reports (event details, budget summary, risk log)
- Export full analytics dashboard as PDF
- Implementation: `WeasyPrint` or `ReportLab`

---

## 8. Technology Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Django 4.x (Python) |
| **Database** | SQLite (development) / PostgreSQL (production) |
| **Frontend** | Django Templates + Bootstrap 5 |
| **Charts** | Chart.js (via CDN) |
| **AI Integration** | Google Gemini API (Python SDK) |
| **PDF Generation** | WeasyPrint or ReportLab |
| **Authentication** | Django Auth (built-in) |
| **Version Control** | Git + GitHub |
| **Deployment** | Local / PythonAnywhere / Render |

---

## 9. Project Methodology

### 9.1 Integrated Management Framework

CEMS uses a hybrid approach combining traditional rigor with Agile flexibility.

**Traditional Project Management**
- Comprehensive feasibility study
- Detailed WBS before development begins
- Precise cost and time estimation

**Agile Scrum**
- 2-day sprints across the 10-day timeline
- Daily standups (async in team chat)
- Sprint review at end of each sprint

**DevOps**
- Git for version control with feature branches
- Structured testing before merges
- Monitoring via Django logging

### 9.2 Work Breakdown Structure (WBS)

```
CEMS Project
├── 1. Planning & Setup
│   ├── 1.1 Requirements finalization
│   ├── 1.2 DB schema design
│   └── 1.3 Project scaffolding
├── 2. Authentication Module
│   ├── 2.1 User model & roles
│   └── 2.2 Login / logout views
├── 3. Event Management Module
│   ├── 3.1 Event CRUD
│   ├── 3.2 Resource assignment
│   └── 3.3 Status management
├── 4. Budget & Risk Module
│   ├── 4.1 Budget tracker
│   └── 4.2 Risk log
├── 5. Dashboard & Analytics
│   ├── 5.1 Summary dashboard
│   └── 5.2 Chart.js charts + heatmap
├── 6. AI & Smart Features
│   ├── 6.1 Gemini description generator
│   ├── 6.2 Smart scheduling
│   └── 6.3 Budget estimator
├── 7. PDF Export
└── 8. Testing & Polish
```

---

## 10. Risk Analysis

| Risk ID | Risk | Probability | Impact | Score | Mitigation |
|---|---|---|---|---|---|
| R01 | Gemini API rate limits or downtime | Medium | High | 6 | Cache responses; fallback to manual description |
| R02 | SQLite not suitable for concurrent users | Low | Medium | 3 | Use PostgreSQL in production |
| R03 | WeasyPrint rendering issues | Medium | Medium | 4 | Fallback to ReportLab |
| R04 | Timeline overrun (10 days) | Medium | High | 6 | Prioritize core features; defer AI if needed |
| R05 | Scope creep from client feedback | Low | High | 4 | Lock scope via this PDR; change requests go through approval |
| R06 | Inaccurate budget estimator predictions | Medium | Low | 3 | Clearly label as estimate; improve with more data over time |

---

## 11. Cost Estimation

> Note: This is a PBL academic project. Costs are estimated for reference.

| Item | Estimated Cost |
|---|---|
| Django development (backend) | ₹0 (open source) |
| Chart.js (frontend charts) | ₹0 (free CDN) |
| Bootstrap 5 (UI) | ₹0 (free CDN) |
| Google Gemini API | Free tier (up to 60 RPM) |
| WeasyPrint / ReportLab | ₹0 (open source) |
| Hosting (PythonAnywhere free tier) | ₹0 |
| **Total Infrastructure Cost** | **₹0 (academic use)** |

---

## 12. Timeline & Milestones

| Sprint | Days | Deliverables |
|---|---|---|
| **Sprint 1** | Days 1–2 | Project setup, Django scaffolding, DB models, auth system (login + 3 roles) |
| **Sprint 2** | Days 3–4 | Event CRUD, resource assignment, status management, budget tracker |
| **Sprint 3** | Days 5–6 | Risk log, dashboard summary cards, Chart.js charts (pie, bar, line) |
| **Sprint 4** | Days 7–8 | Risk heatmap, Gemini API integration, smart scheduling, budget estimator |
| **Sprint 5** | Days 9–10 | PDF export, testing, bug fixing, UI polish, documentation |

**Final Delivery**: Day 10

---

## 13. Expected Outcomes

Upon successful completion, CEMS will deliver:

1. A fully functional, role-based web application for college event management
2. Real-time budget tracking with visual analytics
3. Automated AI-assisted event description generation
4. Smart scheduling to eliminate booking conflicts
5. PDF-exportable event and budget reports
6. A working demonstration of Project Management concepts: WBS, risk analysis, cost estimation, Agile sprints

---

## 14. Assumptions & Constraints

**Assumptions**
- The development team has Python/Django familiarity
- A Google Gemini API key is available for development
- The system will be used by a single college (single-tenant)
- SQLite is acceptable for the demo/prototype phase

**Constraints**
- 10-day development timeline
- No payment gateway
- No mobile application
- No large-scale production deployment required

---

## 15. Sign-Off

| Role | Name | Signature | Date |
|---|---|---|---|
| Project Lead | | | |
| Client Representative (Antigravity) | | | |
| Faculty Advisor | | | |

---

*Document Version 1.0 — College Event Management System PDR — Sterling & Partners*
