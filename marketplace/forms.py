from django import forms

import selectable.forms as selectable

from .lookups import UniversityLookup, ProgrammeLookup, SemesterLookup, CourseLookup

class UniversityForm(forms.Form):
    university = forms.CharField(
        label='Universitet',
        widget=selectable.AutoComboboxWidget(UniversityLookup),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ChainedForm(forms.Form):
    university = forms.CharField(
        label='Universitet',
        widget=selectable.AutoComboboxWidget(UniversityLookup),
        required=False,
    )

    programme = forms.CharField(
        label='Program',
        widget=selectable.AutoComboboxWidget(ProgrammeLookup),
        required=False,
    )

    semester = forms.CharField(
        label='Termin',
        widget=selectable.AutoComboboxWidget(SemesterLookup),
        required=False,
    )

    course = forms.CharField(
        label='Kurs',
        widget=selectable.AutoComboboxWidget(CourseLookup),
        required=False,
    )

    #programme2 = selectable.AutoCompleteSelectField(
    #    lookup_class=ProgrammeLookup,
    #    label='Program2',
    #    required=False,
    #    widget=selectable.AutoComboboxSelectWidget
    #)