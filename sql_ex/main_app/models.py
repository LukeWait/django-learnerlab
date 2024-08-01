from django.db import models

class RecordLabel(models.Model):
    name = models.CharField('Label Name', max_length=100)
    address = models.CharField('Address', max_length=300)
    email = models.EmailField('Contact Email')

    def __str__(self):
        return self.name

class Musician(models.Model):
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    instrument = models.CharField('Instrument', max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.instrument})"

class Album(models.Model):
    title = models.CharField('Album Title', max_length=200)
    artist = models.CharField('Artist', max_length=200)
    release_date = models.DateField('Release Date')
    genre = models.CharField('Genre', max_length=100)
    label = models.ForeignKey(RecordLabel, on_delete=models.CASCADE, verbose_name='Record Label')
    album_members = models.ManyToManyField(Musician, blank=True, verbose_name='Album Members')

    def __str__(self):
        return self.title
