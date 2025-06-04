from django.db import models
from events.models import SubEvent
# Create your models here.
# from datetime import time

# Sport choices for registration
# class Registration(models.Model):
#     SPORT_CHOICES = [
#         ('cricket', 'Cricket'),
#         ('football', 'Football'),
#         ('volleyball', 'Volleyball'),
#         ('kabaddi', 'Kabaddi'),
#         # Add more options as needed
#     ]
    
#     event = models.ForeignKey(SubEvent, on_delete=models.CASCADE)
#     fullname = models.CharField(max_length=50)
#     college = models.CharField(max_length=100)
#     year_of_study = models.CharField(max_length=10)
#     email = models.EmailField(max_length=50)
#     contact_number = models.CharField(max_length=10)
#     emergency_contact = models.CharField(max_length=10)
#     sport = models.CharField(max_length=50, choices=SPORT_CHOICES, default='')

#     def __str__(self):
#         return f"{self.fullname} | {self.email} | {self.contact_number}"


class TeamRegistration(models.Model):
    teamname = models.CharField(max_length=50)
    playername = models.CharField(max_length=50)
    year_of_study = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.teamname.capitalize()}"



class Participant(models.Model):
    DEPT_CHOICES = [
        ('cs', 'CS'),
        ('it', 'IT'),
        ('entc', 'ENTC'),
        ('civil', 'CIVIL'),
        ('mechanical', 'MECHANICAL'),
        ('aids', 'AIDS'),
        ('aiml', 'AIML'),
        ('mba', 'MBA'),
        ('mca', 'MCA'),
        ('pharmacy', 'PHARMACY'),
    ]
    YEAR_OF_STUDY = [
        ('fe', 'FE'),
        ('se', 'SE'),
        ('te', 'TE'),
        ('be', 'BE'),
    ]
    full_name = models.CharField(max_length=100)  # Name of the participant or team leader
    # email = models.EmailField(unique=True)  # Participant's email
    email = models.EmailField()  # Participant's email
    college_name = models.CharField(max_length=100)  # Name of the college
    dept = models.CharField(max_length=50, choices=DEPT_CHOICES, default="")
    year_of_study = models.CharField(max_length=2, choices=YEAR_OF_STUDY, default="")
    contact_number = models.CharField(max_length=10)  # Contact number
    emergency_contact = models.CharField(max_length=10)  # Contact number
    sub_event = models.ForeignKey(SubEvent, on_delete=models.CASCADE, related_name='participants')  # Linked to SubEvent
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        unique_together = ('email', 'sub_event') 

    def __str__(self):
        return f"{self.full_name} ({self.sub_event.name})"
    