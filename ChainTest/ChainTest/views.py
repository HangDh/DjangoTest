from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.shortcuts import render, redirect
from ChainTest.models import Person, City, Task, Order
from ChainTest.forms import PersonForm, TaskCreateForm

class PersonListView(ListView):
    model = Person
    context_object_name = 'people'

class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')

class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')

def load_cities(request):
   country_id = request.GET.get('country')
   cities = City.objects.filter(country_id=country_id).order_by('name')
   return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})

def form_handle(request, template_name = 'ChainTest/task_create.html'):
    form = TaskCreateForm()
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            for k,v in cdata.items():
                if cdata[k] == True:
                    try:
                        Task.objects.create_task(k, Order.objects.get(id=1))
                    except:
                        form.add_error(None, 'Duplicated task: '+ k +' - please try again')
                        return render(request, template_name, {'form': form})
            return redirect('person_changelist')
    return render(request, template_name, {'form': form})
