from django.shortcuts import render
from django.views.generic import ListView
from .models import City
from .forms import CitySearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views import View
from unidecode import unidecode

class CityListView(ListView):
	model = City
	template_name = 'city_list.html'
	paginate_by = 40
	ordering = ['name']

	def get_query(self):
		cities = City.objects.all()

		paginator = Paginator(cities, self.paginate_by, allow_empty_first_page=True)
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
	paginate_by = 40

	def get(self, request):
		form = CitySearchForm()
		page_number = request.GET.get('page')
		if page_number:
			search_term = request.session.get('search_term')
			results = City.objects.filter(name__startswith=search_term).distinct()
			paginator = Paginator(results, self.paginate_by, allow_empty_first_page=True)
			try:
				page_obj = paginator.page(page_number)
			except PageNotAnInteger:
				page_obj = paginator.page(1)
			except EmptyPage:
				page_obj = paginator.page(paginator.num_pages)
			return render(request, 'city_search.html', {'form': form, 'page_obj': page_obj})
		else:
			return render(request, 'city_search.html', {'form': form})

	def post(self, request):
		form = CitySearchForm(request.POST)
		if form.is_valid():
			search_term = unidecode(form.cleaned_data['search_term'])
			request.session['search_term'] = search_term
			if search_term:
				results = City.objects.filter(name__startswith=search_term).distinct()

				paginator = Paginator(results, self.paginate_by, allow_empty_first_page=True)
				page_number = request.GET.get('page', 1)
				try:
					page_obj = paginator.page(page_number)
				except PageNotAnInteger:
					page_obj = paginator.page(1)
				except EmptyPage:
					page_obj = paginator.page(paginator.num_pages)
				return render(request, 'city_search.html', {'form': form, 'page_obj': page_obj})
			else:
				page_obj = Paginator([], self.paginate_by, allow_empty_first_page=True).page(1)
				return render(request, 'city_search.html', {'form': form, 'page_obj': page_obj})
		page_obj = Paginator([], self.paginate_by, allow_empty_first_page=True).page(1)
		return render(request, 'city_search.html', {'form': form, 'page_obj': page_obj})
