<!-- GSD:project-start source:PROJECT.md -->
## Project

**College Event Management System (CEMS)**

A Django-based web platform for planning, scheduling, budgeting, and monitoring academic and cultural events within a college. It serves three user roles — Students, Faculty Coordinators, and Administrators — with a centralized, role-aware interface that replaces manual coordination through emails, spreadsheets, and meetings.

**Core Value:** A centralized event management platform that eliminates schedule conflicts, budget mismanagement, and poor resource coordination by giving every stakeholder real-time visibility into the full event lifecycle.

### Constraints

- **Timeline**: 10-day development sprint — core features must ship within this window
- **Tech Stack**: Django 4.x, Python 3.10+, SQLite (dev) / PostgreSQL (prod), Bootstrap 5, Chart.js
- **AI Dependency**: Gemini API free tier (60 RPM) — must handle rate limits and downtime gracefully
- **PDF System Dependencies**: WeasyPrint requires `libpango` — ReportLab as fallback
- **Single Tenant**: One college only — no multi-tenancy
- **No REST API**: Server-rendered views only — 3 AJAX endpoints for AI features
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
