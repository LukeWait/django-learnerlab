from django.db import models

# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    post_code = models.CharField('Post Code',max_length=4)
    phone = models.CharField('Contact Phone', max_length=10)
    website = models.URLField() 
    email_address = models.EmailField('Email Address')

    def __str__(self) :
        return self.name 

class ClubMember(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self) :
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE) 
    manager = models.CharField(max_length= 50)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(ClubMember, blank =True)

    def __str__(self) :
        return self.name 



