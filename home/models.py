# from django.db import models








# from django.db import models

# class TeamRegistration(models.Model):
#     # team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
#     teamname = models.CharField(max_length=50)
#     playername = models.CharField(max_length=50)
#     year_of_study = models.CharField(max_length=10)
#     contact_number = models.CharField(max_length=10)
    
#     ### teamname = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
#     def __str__(self):
#         # return self.fullname, self.college, self.year_of_study, self.email, self.contact_number, self.emergency_contact
#         return f"{self.playername.capitalize()} ({self.teamname})"


# class EventDetails(models.Model):   
#     number = models.AutoField(primary_key=True)
#     eventname = models.CharField(max_length=50, default='', unique=True)
#     date = models.DateField()
#     time = models.TimeField()
#     # venues = ['College ground', 'Seminar Hall', 'College Campus']
#     # equipments = {
#     #     'Cricket':['Bats', 'Balls', 'Scoreboard'],
#     #     'Football':['Goal Post', 'Footballs', 'Scoreboard'],
#     #     'Volleyball':['Net', 'Voleyballs', 'Scoreboard'],
#     #     'Kabaddi':['Mat', 'Scoreboard'],
#     #     'Badminton':['Net', 'Rackets','Shuttles', 'Scoreboard'],
#     # }
#     # resources = models.CharField(max_length=30, choices=SELECT_RESOURCES, default="")
#     def __str__(self):
#         return str(self.eventname)
    

# class Resources(models.Model):
#     VENUE_CHOICES = [('college ground','College ground'), ('seminar hall','Seminar Hall'), ('college campus','College Campus')]
#     event = models.ForeignKey(EventDetails, on_delete=models.CASCADE, related_name='resources')
#     venue = models.CharField(choices=VENUE_CHOICES, max_length=50, default='College Ground')
#     # venue = models.CharField(max_length=50)
#     # equipments = models.JSONField(default=dict)
#     def clean(self):
#         # Ensure the venue is not double-booked
#         if Resources.objects.filter(
#             venue=self.venue,
#             event__date=self.event.date,
#             event__time=self.event.time
#         ).exists():
#             raise ValidationError("The venue is already booked for this date and time.")

#     def __str__(self):
#         return self.venue
    
# class Equipment(models.Model):
#     name = models.CharField(max_length=50)
#     quantity = models.PositiveIntegerField()
#     event = models.ForeignKey(EventDetails, on_delete=models.CASCADE, related_name='equipment')

#     def __str__(self):
#         return f"{self.name} ({self.quantity}) for {self.event.eventname}"
