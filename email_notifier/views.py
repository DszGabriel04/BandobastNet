from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
from authentication.models import Officer
from django.conf import settings  # Import settings to access DEFAULT_FROM_EMAIL

def send_duty_start_email(officer):
    try:
        subject = "Duty Start Notification"
        message = f"Hello {officer.user_profile.user.username}, your duty starts at {officer.duty_time_start}."
        recipient_list = [officer.user_profile.email]

        # Use the verified email address from settings
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Exception as e:
        print(f"Error sending duty start email: {e}")

def send_duty_end_email(officer):
    try:
        subject = "Duty End Notification"
        message = f"Hello {officer.user_profile.user.username}, your duty ends at {officer.duty_time_end}."
        recipient_list = [officer.user_profile.email]

        # Use the verified email address from settings
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Exception as e:
        print(f"Error sending duty end email: {e}")

def schedule_email(request):
    if request.method == 'POST':
        current_time = timezone.now()
        on_duty_officers = Officer.objects.filter(is_on_duty=True)

        if not on_duty_officers.exists():
            return JsonResponse({'status': 'error', 'message': 'No officers are currently on duty.'}, status=404)

        results = []

        for officer in on_duty_officers:
            if current_time < officer.duty_time_start:
                send_duty_start_email(officer)
                results.append({'officer': officer.user_profile.user.username, 'status': 'Duty start email sent.'})
            elif current_time < officer.duty_time_end:
                send_duty_end_email(officer)
                results.append({'officer': officer.user_profile.user.username, 'status': 'Duty end email sent.'})
            else:
                results.append({'officer': officer.user_profile.user.username, 'status': 'Duty time has already passed.'})

        return JsonResponse({'status': 'success', 'results': results})

    return JsonResponse({'status': 'fail'}, status=400)
