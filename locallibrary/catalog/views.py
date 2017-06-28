from django.shortcuts import render
from django.http import Http404
from django.views import generic

from .models import Book, Author, BookInstance, Genre, Language


def index(request):
    """
    View function for home page of site.
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_visits=request.session.get('num_visits', 0)
    num_books_part_word  = Book.objects.filter(title__contains='Project').count()

    request.session['num_visits'] = num_visits+1

    return render(
        request,
        'catalog/index.html',
        context={'num_books': num_books, 'num_instances': num_instances, 'num_instances_available': num_instances_available,
                 'num_authors': num_authors, 'num_genres':num_genres, 'num_visits':num_visits, 'num_books_part_word':num_books_part_word},
    )


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    paginate_by = 2

    def get_queryset(self):
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = '!!!!!!!This is just some data!!!!!!!!!!'
        return context


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, pk):
        try:
            book_id = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")

        return render(
            request,
            'catalog/book_detail.html',
            context={'book': book_id, },
        )


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'
    paginate_by = 2

    def get_queryset(self):
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['some_data'] = '!!!!!!!This is just some Author!!!!!!!!!!'
        return context


class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, pk):
        try:
            author_obj = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404("Author does not exist!")

        return render(
            request,
            'catalog/author_detail.html'
            #context = {'author': author_obj, },
        )

