from selectable.base import ModelLookup
from selectable.registry import registry

from .models import Book, University, Programme, Semester, Course

class UniversityLookup(ModelLookup):
    model = University
    search_fields = ('name__icontains', )
    order_by = 'name'

class ProgrammeLookup(ModelLookup):
    model = Programme
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super().get_query(request, term)
        university_name = request.GET.get('university', '')

        if university_name != '':
            results = results.filter(university=University.objects.get(name=university_name))
        return results

"""
        programme_set = University.objects.get(name=university_name) \
                        .programme_set.all().order_by('name')

        return programme_set
"""

class SemesterLookup(ModelLookup):
    model = Semester
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super().get_query(request, term)
        university_name = request.GET.get('university', '')
        programme_name = request.GET.get('programme', '')

        if university_name != '' and programme_name != '':
            university = University.objects.get(name=university_name)
            programme_set = university.programme_set.all()

            results = results.filter(programme__name=programme_name)    \
                        .filter(programme__in=programme_set)
        else:
            return results.none()
        return results

"""
        print('----- START SEMESTER LOOKUP ------')
        print('----- RESULTS ------')
        print(results)
        print('----- Uni Name ------')
        print(university_name)
        print('----- Programme name ------')
        print(programme_name)
        print('----- END SEMESTER LOOKUP ------')
"""

"""
    semester_set = University.objects.get(name=university_name) \
                    .programme_set.get(name=programme_name)  \
                    .semester_set.all().order_by('id')

    return semester_set
"""
class CourseLookup(ModelLookup):
    model = Course
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super().get_query(request, term)
        university_name = request.GET.get('university', '')
        programme_name = request.GET.get('programme', '')
        semester_name = request.GET.get('semester', '')

        if university_name != '' and programme_name != '' and semester_name != '':
            university = University.objects.get(name=university_name)
            programme_set = university.programme_set.all()
            programme = programme_set.get(name=programme_name)
            semester = programme.semester_set.get(name=semester_name)

            results = results.filter(university=university)             \
                        .filter(semesters__programme__in=programme_set) \
                        .filter(semesters__name=semester_name)

        else:
            return results.none()
        return results

registry.register(UniversityLookup)
registry.register(ProgrammeLookup)
registry.register(SemesterLookup)
registry.register(CourseLookup)