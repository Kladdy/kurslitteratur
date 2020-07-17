from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

from .models import Book, Programme, University
from .forms import ChainedForm

import isbnlib
import pprint

# Books
class IndexView(generic.ListView):
    template_name = 'marketplace/index.html'
    context_object_name = 'latest_book_list'
    
    def get_queryset(self):
        """
        Return the last five added books
        """
        return Book.objects.order_by('-id')[:5]

class DetailView(generic.DetailView):
    model = Book
    template_name = 'marketplace/detail.html'

def add_book(request):
    return render(request, 'marketplace/add_book.html')

def isbn_lookup(request):
    try:
        # TODO convert ISBN and get metadata
        isbn = request.POST['isbn']

        canonical_isbn = isbnlib.canonical(isbn)
        if isbnlib.is_isbn10(isbn):
            isbn = isbnlib.to_isbn13(isbn)

        if Book.objects.filter(isbn=isbn).count() > 0:
            raise FileExistsError(f'Book with ISBN {isbn} already exists')

        if not isbnlib.is_isbn13(isbn):
            raise ValueError(f'ISBN is not valid: {isbn}')
        else:
            meta = isbnlib.meta(isbn)

        if not meta:
            raise RuntimeError(f'No book found for ISBN: {isbn}')

        assert meta['ISBN-13'] == isbn, 'ISBN of looked up book does not match requested'

        print('------------------------\n Adding book:')    
        print(f'ISBN: {isbn}')
        print(meta)

    except (FileExistsError):
        return render(request, 'marketplace/add_book.html', {
            'isbn': isbn,
            'error_message': "Book already exists",
        })
    except (ValueError):
        return render(request, 'marketplace/add_book.html', {
            'isbn': isbn,
            'error_message': "Invalid ISBN",
        })
        # TODO except if error arises, eg if ISBN is invalid
    except (RuntimeError):
        return render(request, 'marketplace/add_book.html', {
            'isbn': isbn,
            'error_message': "Did not find book with that ISBN",
        })
    except (AssertionError):
        return render(request, 'marketplace/add_book.html', {
            'isbn': isbn,
            'error_message': "The found book did not match the requested ISBN",
        })
    else:
        title = meta['Title']
        authors = meta['Authors']
        publisher = meta['Publisher']
        year = meta['Year']
        language = meta['Language']
        cover_img = f'http://covers.openlibrary.org/b/isbn/{isbn}-M.jpg'

        book = Book.objects.create(
                isbn=isbn,
                title=title,
                authors=authors,
                publisher=publisher,
                year=year,
                language=language,
                cover_img=cover_img
            )
        book.save()
        print(f'Added book {title} to library\n ------------------------')
        # Return to book list
        return HttpResponseRedirect(reverse('marketplace:index'))

# Browsing
def browse(request):

    book_set = []

    if request.GET:
        initial = request.GET

        university = initial.get('university', '')
        programme = initial.get('programme', '')
        semester = initial.get('semester', '')
        course = initial.get('course', '')

        if university != '' and programme != '' and semester != '' and course != '':
            course = University.objects.get(name=university)   \
                        .programme_set.get(name=programme)     \
                        .semester_set.get(name=semester)       \
                        .course_set.get(name=course)           \

            book_set = course.books.all()

        form = ChainedForm(initial=initial)
    else:
        form = ChainedForm()

    context = {
        'form': form,
        'books': book_set
    }

    return render(request, 'marketplace/browse.html', context)