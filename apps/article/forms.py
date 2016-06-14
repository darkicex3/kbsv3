from haystack.forms import SearchForm
from django.forms import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ArticlesSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()


# Apply summernote to specific fields.
class SomeForm(forms.Form):
    foo = forms.CharField(widget=SummernoteWidget())  # instead of forms.Textarea


# If you don't like <iframe>, then use inplace widget
# Or if you're using django-crispy-forms, please use this.
class AnotherForm(forms.Form):
    bar = forms.CharField(widget=SummernoteInplaceWidget())
