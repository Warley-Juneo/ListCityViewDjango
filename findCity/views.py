from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .models import City
from .forms import CitySearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.urls import reverse_lazy

class CityListView(ListView):
	model = City
	template_name = 'city_list.html'
	paginate_by = 40

	def get_query(self):
		cities = City.objects.all()

		paginator = Paginator(cities, self.paginate_by)
		page = self.request.GET.get('page')
		try:
			cities = paginator.page(page)
		except PageNotAnInteger:
			cities = paginator.page(1)
		except EmptyPage:
			cities = paginator.page(paginator.num_pages)
		return cities

	def dispatch(self, request, *args, **kwargs):
		try:
			return super().dispatch(request, *args, **kwargs)
		except Exception as e:
			return HttpResponse(str(e), status=500)


def home(request):
	form = CitySearchForm()
	return render(request, 'city_search.html', {'form': form})


class CitySearchView(FormView):
	template_name = 'city_search.html'
	form_class = CitySearchForm
	success_url = reverse_lazy('city-search')

	def form_valid(self, form):
		search_term = form.cleaned_data['search_term']
		print("Search term:", search_term)
		if search_term:
			self.results = City.objects.filter(name__startswith=search_term).distinct()
		return super().form_valid(form)

	def form_invalid(self, form):
		print("Form errors:", form.errors)
		return super().form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if hasattr(self, 'results'):
			context['results'] = self.results
		return context
