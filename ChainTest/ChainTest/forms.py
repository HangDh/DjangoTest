from django import forms
from ChainTest.models import Person, City, Country

class PersonForm(forms.ModelForm):
   class Meta:
      model = Person
      fields = ('name', 'birthdate', 'country', 'city')

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()