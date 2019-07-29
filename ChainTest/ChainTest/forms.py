from django import forms
from ChainTest.models import Person, City, Country

class PersonForm(forms.ModelForm):
   class Meta:
      model = Person
      fields = ('name', 'birthdate', 'country', 'city')

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

class TaskCreateForm(forms.Form):
    cutting = forms.BooleanField(label='Cięcie piłą', required=False)
    insulating = forms.BooleanField(label='Izomowanie', required=False)
    gaskets = forms.BooleanField(label='Gumownia', required=False)
    frames = forms.BooleanField(label='Montaż ramy', required=False)
    vents = forms.BooleanField(label='Montaż skrzydeł', required=False)
    glass_frames = forms.BooleanField(label='Szklenie ramy', required=False)
    glass_vents = forms.BooleanField(label='Szklenie skrzydeł', required=False)
         