from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from accounts.decorators import faculty_or_admin_required
import json


def _get_gemini_response(prompt):
    """Call Gemini API with rate-limit handling."""
    try:
        import google.generativeai as genai
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return None, "Gemini API key not configured. Set GEMINI_API_KEY in .env"
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"AI service error: {str(e)}"


@login_required
@faculty_or_admin_required
def ai_dashboard(request):
    return render(request, 'ai_features/ai_dashboard.html')


@csrf_exempt
@login_required
def generate_description(request):
    """AJAX: Generate event description using Gemini."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        name = data.get('name', '')
        category = data.get('category', '')
        prompt = f"""Generate a professional, engaging event description for a college event.
Event Name: {name}
Category: {category}
Write 2-3 sentences that are compelling and informative. Include what attendees can expect.
Return ONLY the description text, no extra formatting."""
        text, error = _get_gemini_response(prompt)
        if error:
            return JsonResponse({'error': error}, status=500)
        return JsonResponse({'description': text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@login_required
def smart_schedule(request):
    """AJAX: Get smart scheduling suggestions using Gemini."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        event_name = data.get('name', '')
        category = data.get('category', '')
        duration = data.get('duration', '2 hours')
        from events.models import Event
        existing = list(Event.objects.filter(status__in=['planned', 'in_progress']).values('name', 'date', 'start_time', 'end_time', 'venue')[:20])
        existing_str = "\n".join([f"- {e['name']} on {e['date']} {e['start_time']}-{e['end_time']} at {e['venue']}" for e in existing]) or "No existing events."

        prompt = f"""As a college event scheduling assistant, suggest 3 optimal time slots for this event.
Event: {event_name} (Category: {category}, Duration: {duration})
Existing Events:
{existing_str}
Consider: avoid conflicts, prefer weekday evenings for academic events, weekends for cultural.
Format each suggestion as: Date, Time, Reason (one per line)."""
        text, error = _get_gemini_response(prompt)
        if error:
            return JsonResponse({'error': error}, status=500)
        return JsonResponse({'suggestions': text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@login_required
def estimate_budget(request):
    """AJAX: Estimate budget breakdown using Gemini."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        event_name = data.get('name', '')
        category = data.get('category', '')
        attendees = data.get('attendees', 100)
        prompt = f"""As a college event budget advisor, provide a budget estimate breakdown.
Event: {event_name} (Category: {category})
Expected Attendees: {attendees}
Provide estimates in Indian Rupees (₹) for these categories:
- Venue & Logistics
- Catering
- Marketing & Promotion
- Equipment & Tech
- Decoration
- Speaker/Honorarium
- Transport
- Miscellaneous
Format: Category: ₹amount (one per line), followed by Total."""
        text, error = _get_gemini_response(prompt)
        if error:
            return JsonResponse({'error': error}, status=500)
        return JsonResponse({'estimate': text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
