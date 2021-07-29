import datetime

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from booking.models import SessionBooking, DoctorConfirmedSlots, PatientPlan
from users.models import Patient


def generate_link():
    import requests
    url = "https://api.zoom.us/v2/users/creation.satya@gmail.com/meetings"
    payload = {'topic': 'YourPhysio demo session',
               'type': '2',
               'pre_schedule': 'true',
               'start_time': '2021-07-28 14:48:00.340484+00',
               'duration': '5',
               'timezone': 'IN',
               'password': 'u*Tan&rdrh(3HEa',
               'agenda': 'meetng with Knee consulatant',
               'tracking_fields': '[{"field":"utm","value":"UTM123"},{"field":"utm_Campaign","value":"utmc234"}]',
               'recurrence': '{"type":"<integer>","repeat_interval":"<integer>","weekly_days":"1","monthly_day":1,"monthly_week":"<integer>","monthly_week_day":"<integer>","end_times":1,"end_date_time":"<dateTime>"}',
               'settings': '{"host_video":true,"participant_video":true,"cn_meeting":false,"in_meeting":false,"join_before_host":true,"jbh_time":10,"mute_upon_entry":false,"watermark":false,"use_pmi":false,"approval_type":2,"registration_type":1,"audio":"both","auto_recording":"none","alternative_hosts":"<string>","close_registration":false,"waiting_room":"<boolean>","global_dial_in_countries":["<string>","<string>"],"contact_name":"<string>","contact_email":"<string>","registrants_email_notification":"<boolean>","registrants_confirmation_email":"<boolean>","meeting_authentication":"<boolean>","authentication_option":"<string>","authentication_domains":"<string>","authentication_exception":[{"name":"<string>","email":"<email>"},{"name":"<string>","email":"<email>"}],"additional_data_center_regions":["<string>","<string>"],"breakout_room":{"enable":"<boolean>","rooms":[{"name":"<string>","participants":["<string>","<string>"]},{"name":"<string>","participants":["<string>","<string>"]}]},"language_interpretation":{"enable":"<boolean>","interpreters":[{"email":"<email>","languages":"<string>"},{"email":"<email>","languages":"<string>"}]},"show_share_button":"<boolean>","allow_multiple_devices":"<boolean>","encryption_type":"<string>","approved_or_denied_countries_or_regions":{"enable":"<boolean>","method":"<string>","approved_list":["<string>","<string>"],"denied_list":["<string>","<string>"]},"alternative_hosts_email_notification":true}',
               'template_id': 'satyatempl'}
    files = [

    ]
    headers = {
        'Content-Type': 'multipart/form-data'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return Response(data={"Hello"},status=status.HTTP_200_OK)


@api_view(['GET'])
def return_slots_available_on_a_day_for_a_doctor(request):
    # get active(is_attended=false) booked sesssions
    # get doctor confirmed slots
    # get available slots of them
    # remove booked sessions time from available slots
    # return
    doctor_id  = request.data.get('doctor_id',None)
    current_date = request.data.get('date',None)
    if doctor_id:
        active_booked_sessions = SessionBooking.objects.filter(doctor = doctor_id)
    else:
        return Response("No doctor selected",status=status.HTTP_400_BAD_REQUEST)
    if current_date:
        # get slots confirmed by a doctor as available
        doctor_confirmed_slots = DoctorConfirmedSlots.objects.filter(start_date__range=(current_date, current_date + datetime.timedelta(days=1)),start_date__gte=datetime.datetime.now())

    # get active confirmed slots
    sessions=[]
    for slot in doctor_confirmed_slots:
        dict={}
        dict['start_time'] = slot.start_time
        dict['end_time'] = slot.end_time
        dict['slot_name'] =str(slot.start_time.hour) + "-" + str(slot.end_time.hour)
        is_booked=False
        for session in active_booked_sessions:
            if slot.start_time == session.start_time and slot.end_time == session.end_time:
                is_booked=True
        if is_booked:
            dict['available']=False
        else:
            dict['available']=True
        sessions.append(dict)
    return Response(data = {sessions}, status=status.HTTP_200_OK)





@api_view(['GET'])
def book_slot_for_user(request):
    try:
        patient_id = request.data.get('patient_id',None)
        start_time = request.data.get('start_time',None)
        end_time = request.data.get('end_time',None)
        plan = request.data.get('plan',None)
        video_conferencing_link = generate_link()

        remarks = request.data.get('remarks',None)
        doctor_id = request.data.get('doctor_id',None) # Assuming he can book any doctor
        if plan:
            plan = PatientPlan.objects.filter(plan=plan)
            bookings = SessionBooking.objects.filter(plan=plan,is_attended=True)

        if patient_id and start_time and end_time:
            patient = Patient.objects.filter(id = patient_id)
            SessionBooking.objects.create(plan=plan,start_time=start_time,end_time=end_time,video_conferencing_link=video_conferencing_link,session=len(bookings),remarks=remarks,date_of_booking=datetime.datetime.now(),doctor_id=doctor_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    message = "Your session is booked for f'start_time' . Confirmed . Please be ready with given equipments "
    send_scheduled_message(patient,message,start_time)
    return Response(status=status.HTTP_200_OK)



def send_scheduled_message(user,message,scheduled_date):
    import requests
    return requests.post(
    "https://api.mailgun.net/v2/samples.mailgun.org/messages",
    auth=("api", "key-3ax6xnjp29jd6fds4gc373sgvjxteol0"),
    data={"from": "Yourphysio <me@samples.mailgun.org>",
      "to": user.email,
      "subject": "Session Booked",
      "text": message,
      "o:deliverytime": str(scheduled_date)})