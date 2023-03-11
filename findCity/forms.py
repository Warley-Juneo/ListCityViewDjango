from django import forms

class CitySearchForm(forms.Form):
	search_term = forms.CharField(label='Search')
