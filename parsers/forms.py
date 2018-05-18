from django import forms
import re


class NewQueryFrom(forms.Form):
    author = forms.CharField(max_length=255, required=False)
    title = forms.CharField(max_length=255, required=False)
    keywords = forms.CharField(max_length=255, required=False)
    year1 = forms.CharField(max_length=4, required=False)
    year2 = forms.CharField(max_length=4, required=False)

    def clean(self):
        year1 = self.cleaned_data.get('year1')
        year2 = self.cleaned_data.get('year2')
        if year2 and year1 and year2 < year1:
            raise forms.ValidationError('Неверно указан год')

    # def clean_author(self):
    #     author = self.cleaned_data.get('author')
    #     pattern = r'^[А-Я][а-я]+ [А-Я]\. [А-Я]\.$'
    #     if re.match(pattern, author):
    #         return author
    #     raise forms.ValidationError('Имя автора некорректно')
