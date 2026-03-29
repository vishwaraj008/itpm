from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum, Count
from events.models import Event
from budget.models import BudgetItem
from risks.models import Risk
import io


def _generate_pdf_reportlab(html_content, title="Report"):
    """Generate PDF using ReportLab (no system dependencies)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(name='CFTitle', fontName='Helvetica-Bold', fontSize=24,
                              textColor=HexColor('#5257a8'), spaceAfter=20))
    styles.add(ParagraphStyle(name='CFHeading', fontName='Helvetica-Bold', fontSize=14,
                              textColor=HexColor('#2d3337'), spaceAfter=10, spaceBefore=20))
    styles.add(ParagraphStyle(name='CFBody', fontName='Helvetica', fontSize=10,
                              textColor=HexColor('#596063'), spaceAfter=6, leading=14))

    return buffer, doc, styles


@login_required
def export_event_pdf(request, event_id):
    """Export single event as PDF."""
    event = get_object_or_404(Event, id=event_id)
    budget_items = event.budget_items.all()
    risks = event.risks.all()
    resources = event.event_resources.select_related('resource').all()

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='CFTitle', fontName='Helvetica-Bold', fontSize=22,
                                  textColor=HexColor('#5257a8'), spaceAfter=20))
        styles.add(ParagraphStyle(name='CFH2', fontName='Helvetica-Bold', fontSize=13,
                                  textColor=HexColor('#2d3337'), spaceAfter=8, spaceBefore=16))
        styles.add(ParagraphStyle(name='CFBody', fontName='Helvetica', fontSize=10,
                                  textColor=HexColor('#596063'), spaceAfter=4, leading=14))
        elements = []

        # Header
        elements.append(Paragraph("CampusFlow — Event Report", styles['CFTitle']))
        elements.append(Paragraph(event.name, ParagraphStyle('EventName', fontName='Helvetica-Bold',
                                  fontSize=16, textColor=HexColor('#2d3337'), spaceAfter=12)))

        # Event Details Table
        elements.append(Paragraph("Event Details", styles['CFH2']))
        details_data = [
            ['Category', event.get_category_display(), 'Status', event.get_status_display()],
            ['Date', str(event.date), 'Time', f"{event.start_time} - {event.end_time}"],
            ['Venue', event.venue, 'Organizer', f"{event.organizer.first_name} {event.organizer.last_name}"],
            ['Attendees', str(event.expected_attendees), 'Est. Budget', f"₹{event.estimated_budget}"],
        ]
        t = Table(details_data, colWidths=[2.5*cm, 5*cm, 2.5*cm, 5*cm])
        t.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#596063')),
            ('TEXTCOLOR', (2, 0), (2, -1), HexColor('#596063')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(t)

        if event.description:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph("Description", styles['CFH2']))
            elements.append(Paragraph(event.description, styles['CFBody']))

        # Budget Items
        if budget_items:
            elements.append(Paragraph("Budget Items", styles['CFH2']))
            budget_data = [['Category', 'Description', 'Amount', 'Status']]
            for item in budget_items:
                budget_data.append([item.get_category_display(), item.description, f"₹{item.amount}", item.get_status_display()])
            budget_data.append(['', '', f'Total: ₹{event.total_spent}', ''])
            bt = Table(budget_data, colWidths=[3.5*cm, 6*cm, 3*cm, 2.5*cm])
            bt.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#eef2ff')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ]))
            elements.append(bt)

        # Risks
        if risks:
            elements.append(Paragraph("Risk Register", styles['CFH2']))
            risk_data = [['Title', 'Severity', 'Status', 'Owner']]
            for risk in risks:
                risk_data.append([risk.title, risk.get_severity_display(), risk.get_status_display(), risk.owner.first_name if risk.owner else '—'])
            rt = Table(risk_data, colWidths=[5*cm, 3*cm, 3*cm, 4*cm])
            rt.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#eef2ff')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
            ]))
            elements.append(rt)

        doc.build(elements)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="event_{event.name.replace(" ", "_")}.pdf"'
        return response

    except ImportError:
        return HttpResponse("ReportLab not installed. Run: pip install reportlab", status=500)


@login_required
def export_analytics_pdf(request):
    """Export analytics summary as PDF."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='CFTitle', fontName='Helvetica-Bold', fontSize=22,
                                  textColor=HexColor('#5257a8'), spaceAfter=20))
        styles.add(ParagraphStyle(name='CFH2', fontName='Helvetica-Bold', fontSize=13,
                                  textColor=HexColor('#2d3337'), spaceAfter=8, spaceBefore=16))
        styles.add(ParagraphStyle(name='CFBody', fontName='Helvetica', fontSize=10,
                                  textColor=HexColor('#596063'), spaceAfter=4, leading=14))
        elements = []

        elements.append(Paragraph("CampusFlow — Analytics Report", styles['CFTitle']))

        # Summary stats
        total_events = Event.objects.count()
        total_spent = BudgetItem.objects.aggregate(t=Sum('amount'))['t'] or 0
        total_estimated = Event.objects.aggregate(t=Sum('estimated_budget'))['t'] or 0
        open_risks = Risk.objects.filter(status='open').count()

        summary_data = [
            ['Total Events', str(total_events), 'Total Estimated Budget', f'₹{total_estimated}'],
            ['Planned', str(Event.objects.filter(status='planned').count()), 'Total Spent', f'₹{total_spent}'],
            ['Completed', str(Event.objects.filter(status='completed').count()), 'Open Risks', str(open_risks)],
        ]
        elements.append(Paragraph("Summary", styles['CFH2']))
        st = Table(summary_data, colWidths=[4*cm, 3.5*cm, 4*cm, 3.5*cm])
        st.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(st)

        # Events Table
        events = Event.objects.all()[:20]
        if events:
            elements.append(Paragraph("Events", styles['CFH2']))
            event_data = [['Name', 'Date', 'Category', 'Status', 'Budget']]
            for e in events:
                event_data.append([e.name[:30], str(e.date), e.get_category_display(), e.get_status_display(), f'₹{e.estimated_budget}'])
            et = Table(event_data, colWidths=[5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
            et.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#eef2ff')),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
            ]))
            elements.append(et)

        doc.build(elements)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="campusflow_analytics.pdf"'
        return response

    except ImportError:
        return HttpResponse("ReportLab not installed. Run: pip install reportlab", status=500)
