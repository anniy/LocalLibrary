import uuid

from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class Genre(models.Model):
    """
    Model representing a book Genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre.")

    def __str__(self):
        """
        String for representing the Model object (in Admin).
        """
        return self.name


class Language(models.Model):
    """
    Model represent a Language (e.g English, French, Japanese)
    """
    name = models.CharField(max_length=200, default='English', help_text="Enter the written language of the book .")

    def __str__(self):
        """
        String to represent the Model object (in Admin).
        """
        return self.name


class Author(models.Model):
    """"
    Model representing an author
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['-last_name']

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])


class Book(models.Model):
    """
    Model representing a Book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=1000, help_text="Enter a book title.")
    author = models.ManyToManyField(Author, help_text="Select a author.")
    summary = models.TextField(max_length=2000, help_text="Enter a brief description of the book.")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>.')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book.")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, help_text="Select a writen language.")

    class Meta:
        ordering = ['-title']

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_author(self):
        """
        Create a string of a Genre. This is required to display genre in Admin.
        """
        return ', '.join([author.name for author in self.author.all()[:]])
        display_author.short_description = 'Author'

    def display_genre(self):
        """
        Create a string of a Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
        display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Model representing a specific copy of book (that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library.")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, help_text="Version details (specific release) of the book.")
    due_back = models.DateField(null=True, blank=True, help_text="Date at which the book is expected to come available.")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text="Book availability.")

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id, self.book.title)

