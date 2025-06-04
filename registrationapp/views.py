# Create your views here.
import json
from django.http import HttpResponse, JsonResponse
import openpyxl
from django.shortcuts import get_object_or_404, render, redirect
# from django.views.generic import CreateView
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from .models import Participant, TeamRegistration
from events.models import SubEvent
from .forms import RegistrationForm, TeamRegistrationForm, PlayerFormSet  # Ensure this form exists


# class ParticipantCreateView(CreateView):
#     model = Participant
#     fields = ['full_name', 'email', 'contact_number', 'sub_event', 'college_name']
#     success_url = 'events/'  # Redirect to main event list after registration

class ParticipantListView(ListView):
    model = Participant
    template_name = "view-participants.html"
    context_object_name = "view_participants"

class ParticipantCreateView(View):
    template_name = 'participant_register.html'
    
    def get(self, request, sub_event_id):
        sub_event = get_object_or_404(SubEvent, id=sub_event_id)  # Fetch the sub-event
        form = RegistrationForm(initial={'sub_event': sub_event})  # Pre-fill sub-event
        return render(request, self.template_name, {'form': form, 'sub_event': sub_event, 'fees': sub_event.fees})
    
    def post(self, request, sub_event_id):
        sub_event = get_object_or_404(SubEvent, id=sub_event_id)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.sub_event = sub_event  # Ensure the correct sub-event is saved
            participant.save()
            return JsonResponse({"success": True, "payment_id": participant.payment_id})  # Redirect after successful registration
        return render(request, self.template_name, {'form': form, 'sub_event': sub_event, 'fees': sub_event.fees})

def success_page(request):
    if request.method == 'POST':
        try:
            print("🔹 Received POST request:", request.body)  
            data = json.loads(request.body)
            payment_id = data.get("razorpay_payment_id")
            full_name = data.get("name")
            email = data.get("email")
            college_name = data.get("college_name")
            dept = data.get("dept")
            year_of_study = data.get("year_of_study")
            contact_number = data.get("contact_number")
            emergency_contact = data.get("emergency_contact")
            sub_event_name = data.get("sub_event")
            fees = data.get("fees")

            if not payment_id:
                print("❌ Error: Missing Payment ID")
                return JsonResponse({"success": False, "message": "Payment ID missing"})
            
              # Debugging - Check if all required fields exist
            print(f"✅ Payment ID: {payment_id}")
            print(f"✅ Sub-Event Name: {sub_event_name}")
            print(f"✅ Participant: {full_name}, Email: {email}")

            sub_event = get_object_or_404(SubEvent, name=sub_event_name)
            participant, created = Participant.objects.get_or_create(
                full_name=full_name,
                email=email,
                college_name=college_name,
                dept = dept,
                year_of_study=year_of_study,
                contact_number=contact_number,
                emergency_contact=emergency_contact,
                sub_event=sub_event,
                defaults={"payment_id": payment_id}
            )
            if not created:
                print("⚠️ Warning: Duplicate registration detected")
                return JsonResponse({"success": True, "payment_id": payment_id})
            
            print("✅ Registration successful!")
            return JsonResponse({"success": True, "payment_id": payment_id})
        
        except Exception as e:
            print(f"❌ Exception: {str(e)}") 
            return JsonResponse({"success": False, "message": str(e)})
        
    elif request.method == "GET":
        payment_id = request.GET.get("payment_id")
        if not payment_id:
            return render(request, "error.html", {"message": "Invalid access. No payment ID provided."})

        registration = get_object_or_404(Participant, payment_id=payment_id)
        fees = registration.sub_event.fees
        return render(request, "success.html", {"registration": registration, "fees": fees})


def download_participants_excel(request):
    # Create an Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Participants"

    # Define column headers
    headers = ["Name", "College Name", "Dept", "Year of Study", "Contact", "Emergency Contact"]
    sheet.append(headers)  # Add headers to the first row

    # Fetch participant data and write to Excel rows
    participants = Participant.objects.all()
    for participant in participants:
        sheet.append([
            participant.full_name,
            participant.college_name,
            participant.dept,
            participant.year_of_study,
            participant.contact_number,
            participant.emergency_contact
        ])

    # Prepare the HTTP response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="participants.xlsx"'

    # Save the workbook to the response
    workbook.save(response)
    return response



# def register_participant(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success')  # Redirect to success page
#     else:
#         form = RegistrationForm()
    
#     return render(request, 'registration.html', {'form': form})

# def registration(request):
#     if (request.method == 'POST'):
#         form = RegistrationForm(request.POST)
        
#         if (form.is_valid()):
#             name = form.cleaned_data['fullname']
#             college = form.cleaned_data['college']
#             year_of_study = form.cleaned_data['year_of_study']
#             email = form.cleaned_data['email']
#             contact_number = form.cleaned_data['contact_number']
#             emergency_contact = form.cleaned_data['emergency_contact']

#             participant = Registration.objects.create(fullname=name, college=college, year_of_study=year_of_study, email=email, contact_number=contact_number, emergency_contact=emergency_contact)
#             participant.save()
#             # return render(request,'success.html')
#             return redirect('teamRegistration')
#     form = RegistrationForm()
#     return render(request, "templates/registration.html", {'form': form})

def teamRegistration(request):
    if (request.method == 'POST'):
        form = TeamRegistrationForm(request.POST)
        player_formset = PlayerFormSet(request.POST)

        if (form.is_valid() and player_formset.is_valid()):
             # Extract data manually from the form
            teamname = form.cleaned_data['teamname']
            # team = TeamRegistration.objects.create(teamname=teamname)
            # team = form.save()

            # teamname = form.cleaned_data['teamname']
            for player_form in player_formset:
                if player_form.cleaned_data:
                    playername = form.cleaned_data['playername']
                    year_of_study = form.cleaned_data['year_of_study']
                    contact_number = form.cleaned_data['contact_number']

                    player = TeamRegistration.objects.create(teamname=teamname, playername=playername, year_of_study=year_of_study, contact_number=contact_number)
                    player.save()
            return render(request,'success.html')
    form = TeamRegistrationForm()
    player_formset = PlayerFormSet()
    return render(request, "register_team.html", {'form': form, 'player_formset': player_formset})

