from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200,
    unique=True, 
    help_text="Please enter the book genre")

    class Meta:
        constraints = [
            UniqueConstraint(Lower("name"),name="genre_case_insensitive_constraint",violation_error_message="Genre already exists(Case insensitive match)")
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre-detail',args=[str(self.id)])

class Book(models.Model):
    title = models.CharField(max_length=200)

    author= models.ForeignKey('Author',on_delete=models.RESTRICT,null=True, related_name='authorbooks')

    summary= models.TextField(max_length=2000,help_text="Enter a brief description of the book")

    isbn = models.CharField('ISBN',max_length=13, unique=True,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    genre = models.ManyToManyField(Genre,help_text="Select a genre for this book" )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail",args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

    
class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,  help_text="Unique ID for for this particular book across the whole library")

    book = models.ForeignKey(Book,on_delete=models.RESTRICT,null=True,related_name='instances')

    imprint = models.CharField(max_length=100)

    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On Loan'),
        ('a',"Available"),
        ('r','Reserved')
    )

    status = models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,null=True,default='m')

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['due_back']
        permissions = [('can_mark_returned','Set book as returned')]

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=100)

    last_name =  models.CharField(max_length =100) 

    date_of_birth = models.DateField(null=True,blank=True)

    date_of_death = models.DateField(null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('author-detail',args=[str(self.id)]) 

class Language(models.Model):
    name = models.CharField(max_length=200,unique=True,help_text="Please enter language of the book(e.g. English,French, Japanese , etc. )")

    def get_absolute_url(self):
        return reverse('language-detail',args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_constraint',
                violation_error_message="Language already exists( case insensitive match)"
            )
        ]


