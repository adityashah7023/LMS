from django.db import models
import datetime
from django.contrib.auth.models import User
import os

def get_image_path(instance, filename):
    return os.path.join('libapp/static/libapp/photos', filename)

# Create your models here.
class Libuser(User):
    PROVINCE_CHOICES = (
        ('AB','Alberta'),  # The first value is actually stored in db, the second is descriptive
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    postalcode = models.CharField(max_length=7, null=True, blank=True)
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    phone = models.IntegerField(null=True)
    profile_image=models.ImageField(upload_to='photos/',default='photos/user.png',blank=True,null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Libitem(models.Model):
    TYPE_CHOICES = (
        ('Book', 'Book'),
        ('DVD','DVD'),
        ('Other', 'Other'),
    )
    title = models.CharField(max_length=100)
    itemtype = models.CharField(max_length=6, choices=TYPE_CHOICES, default='Book')
    checked_out=models.BooleanField(default=False)
    user=models.ForeignKey(Libuser, default=None, null=True, blank=True)
    duedate=models.DateField(default=None, null=True, blank=True)
    last_chkout = models.DateField(default=None, null=True, blank=True)
    num_chkout = models.IntegerField(default=0, null=False, blank=False)
    date_acquired = models.DateField(default=datetime.date.today())
    pubyr = models.IntegerField()

    def overdue(self):
        if self.checked_out == True:
            if self.duedate < datetime.date.today():
                return 'Yes'
            else:
                return 'No'
    overdue.short_description='overdue'

    def __str__(self):
        return self.itemtype + ' : ' + self.title

class Book(Libitem):
    CATEGORY_CHOICES = (
        (1, 'Fiction'),
        (2, 'Biography'),
        (3, 'Self Help'),
        (4, 'Education'),
        (5, 'Children'),
        (6, 'Teen'),
        (7, 'Other'),
    )
    author = models.CharField(max_length=100)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)

    def __str__(self):
        return self.title + ' by ' + self.author

class Dvd(Libitem):
    RATING_CHOICE = (
        (1, 'G'),
        (2, 'PG'),
        (3, 'PG-13'),
        (4, '14A'),
        (5, 'R'),
        (6, 'NR'),
    )
    maker = models.CharField(max_length=100)
    duration = models.IntegerField()
    rating = models.IntegerField(choices=RATING_CHOICE,default=1)

    def __str__(self):
        return self.title + ' by ' + self.maker + ' in {0}'.format(self.pubyr)

class Suggestion(models.Model):

    TYPE_CHOICES = (
        (1, 'Book'),
        (2,'DVD'),
        (3, 'Other'),
    )
    title = models.CharField(max_length=100)
    pubyr = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(default=1, choices=TYPE_CHOICES)
    cost = models.IntegerField()
    num_interested = models.IntegerField()
    comments = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.get_type_display() + ' : ' + self.title