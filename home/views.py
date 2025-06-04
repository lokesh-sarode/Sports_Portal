from django.shortcuts import render, redirect
# from .forms import RegistrationForm, TeamRegistrationForm, PlayerFormSet
# from .models import Registration, TeamRegistration
 
# Create your views here.
def index(request):
    return render(request, "index.html")

def events(request):
    venues = ['College ground', 'Seminar Hall', 'College Campus']
    equipments = {
        'Cricket':['Bats', 'Balls', 'Scoreboard'],
        'Football':['Goal Post', 'Footballs', 'Scoreboard'],
        'Volleyball':['Net', 'Voleyballs', 'Scoreboard'],
        'Kabaddi':['Mat', 'Scoreboard'],
        'Badminton':['Net', 'Rackets','Shuttles', 'Scoreboard'],
    }
    
    params = {"eventlist":["a", "b", "c"], "age": 22}
    return render(request, "events.html", params)

def sports(request):
    return render(request, "sports.html")

def teams(request):
    
    return render(request, "teams.html")

def organisers(request):
    return render(request, "organisers.html")

def contactus(request):
    return render(request, "contactus.html")

def aboutus(request):
    return render(request, "aboutus.html")

def privacy_terms(request):
    return render(request, "privacy_and_terms.html")
