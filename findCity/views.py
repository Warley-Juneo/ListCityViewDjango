from django.shortcuts import render
from django.views.generic import ListView
from .models import City
from .forms import CitySearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views import View

class CityListView(ListView):
	model = City
	template_name = 'city_list.html'
	paginate_by = 40
	ordering = ['name']

	def get_query(self):
		cities = City.objects.all()

		paginator = Paginator(cities, self.paginate_by, allow_empity_first_page = True)
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

class CitySearchView(View):
	def get(self, request):
		form = CitySearchForm()
		return render(request, 'city_search.html', {'form': form})

	def post(self, request):
		form = CitySearchForm(request.POST)
		if form.is_valid():
			search_term = form.cleaned_data['search_term']
			print("Search term:", search_term)
			if search_term:
				results = City.objects.filter(name__startswith=search_term).distinct()
				# print o tamnho de result
				print("Results:", len(results))
				return render(request, 'city_search.html', {'form': form, 'results': results})
		return render(request, 'city_search.html', {'form': form})
