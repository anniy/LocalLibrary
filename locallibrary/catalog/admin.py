from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Genre)
admin.site.register(Language)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death')]
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_genre', 'display_author')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status',  'borrower', 'due_back')
    list_filter = ('book', 'status', 'due_back')
    fieldsets = (
        (None, {'fields': ('book','imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back', 'borrower')}),
    )



