# <project>/<app>/management/commands/seed.py
# CODE BY https://stackoverflow.com/questions/51577441/how-to-seed-django-project-insert-a-bunch-of-data-into-the-project-for-initi
from django.core.management.base import BaseCommand

import isbnlib

from marketplace.models import Book, University, Programme, Semester, Course

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any objects """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        print('Seeding data...')
        run_seed(self, options['mode'])
        print('Done!')


def clear_data():
    """Deletes all the table data"""
    print("Delete Book instances")
    Book.objects.all().delete()
    print("Delete University instances")
    University.objects.all().delete()
    print("Delete Programme instances")
    Programme.objects.all().delete()
    print("Delete Semester instances")
    Semester.objects.all().delete()
    print("Delete Course instances")
    Course.objects.all().delete()

def create_book(isbn):
    """Create books from ISBNs"""
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
    print(f'Added book {title}.')
    return book

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """

    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating books
    physics_handbook = create_book('9789144128061')
    error_analysis = create_book('0-935702-75-X')
    calculus = create_book('9780134154367')
    quantum = create_book('9781107189638')
    spec_rel = create_book('0198539533')
    particle_book = create_book('9781118912164')
    print('Added books')

    # Creating universities
    uppsala_university = University.objects.create(name='Uppsala Universitet', city='Uppsala', country='Sweden')
    uppsala_university.save() 
    lulea_university = University.objects.create(name='Luleå Tekniska Universitet', city='Luleå', country='Sweden')
    lulea_university.save()
    kth_university = University.objects.create(name='Kungliga Tekniska Högskolan', city='Stockholm', country='Sweden')
    kth_university.save()
    goteborg_university = University.objects.create(name='Göteborgs Universitet', city='Göteborg', country='Sweden')
    goteborg_university.save()
    lund_university = University.objects.create(name='Lunds Universitet', city='Lund', country='Sweden')
    lund_university.save()
    print('Created universities')

    # Creating programmes
    kandfy = Programme.objects.create(name='Kandidatprogrammet i Fysik', field='Fysik', code='TFY1K', university=uppsala_university)
    apotekare = Programme.objects.create(name='Apotekarprogrammet', field='Farmaci', code='FAO2Y', university=uppsala_university)
    print('Created Kandidatprogrammet i Fysik and Apotekare')

    # Creating semesters
    KF1 = Semester.objects.create(name='KandFy1 - T1', year=1, term=1, programme=kandfy)
    KF2 = Semester.objects.create(name='KandFy1 - T2', year=1, term=2, programme=kandfy)
    KF3 = Semester.objects.create(name='KandFy2 - T3', year=2, term=1, programme=kandfy)
    KF4 = Semester.objects.create(name='KandFy2 - T4', year=2, term=2, programme=kandfy)
    KF5 = Semester.objects.create(name='KandFy3 - T5', year=3, term=1, programme=kandfy)
    KF6 = Semester.objects.create(name='KandFy4 - T6', year=3, term=2, programme=kandfy)

    A1 = Semester.objects.create(name='A1', year=1, term=1, programme=apotekare)
    A2 = Semester.objects.create(name='A2', year=1, term=2, programme=apotekare)
    A3 = Semester.objects.create(name='A3', year=2, term=1, programme=apotekare)
    A4 = Semester.objects.create(name='A4', year=2, term=2, programme=apotekare)
    A5 = Semester.objects.create(name='A5', year=3, term=1, programme=apotekare)
    A6 = Semester.objects.create(name='A6', year=3, term=2, programme=apotekare)
    A7 = Semester.objects.create(name='A7', year=4, term=1, programme=apotekare)
    A8 = Semester.objects.create(name='A8', year=4, term=2, programme=apotekare)
    A9 = Semester.objects.create(name='A9', year=5, term=1, programme=apotekare)
    A10 = Semester.objects.create(name='A10', year=5, term=2, programme=apotekare)
    print('Created KandFy T1-T6 and A1-A10')

    # Creating courses
    mek_kf = Course.objects.create(name='Mekanik KF', code='1FA602', university=uppsala_university) 
    exp_meth_phys = Course.objects.create(name='Experimentell metodik för fysik I', code='1FA608', university=uppsala_university) 
    goa_III = Course.objects.create(name='Geometri och Analys III', code='1MA212', university=uppsala_university) 
    quantum_mech = Course.objects.create(name='Kvantfysik', code='1FA521', university=uppsala_university) 
    special_relativity = Course.objects.create(name='Speciell relativitetsteori', code='1FA156', university=uppsala_university) 
    paricle_physics = Course.objects.create(name='Partikelfysik', code='1FA347', university=uppsala_university) 
    
    print('Created courses')

    # Adding courses to semesters
    KF1.course_set.add(mek_kf)
    KF2.course_set.add(exp_meth_phys)
    KF3.course_set.add(goa_III)
    KF4.course_set.add(quantum_mech)
    KF5.course_set.add(special_relativity)
    KF6.course_set.add(paricle_physics)
    print('Added courses to semesters')

    # Adding books to courses
    mek_kf.books.add(physics_handbook)
    exp_meth_phys.books.add(error_analysis)
    exp_meth_phys.books.add(physics_handbook)
    goa_III.books.add(calculus)
    quantum_mech.books.add(quantum)
    quantum_mech.books.add(physics_handbook)
    special_relativity.books.add(spec_rel)
    special_relativity.books.add(physics_handbook)
    paricle_physics.books.add(particle_book)
    paricle_physics.books.add(physics_handbook)
    print('Added books to semesters')

 