from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        qs = Article.objects.filter(title__icontains=title) #check if null value exists
        if qs.exists():
            self.add_error("title", f"{title} is already in use.")
            print("already is use")
        return data



# class ArticleFormOld(forms.Form):
#     title = forms.CharField()
#     content = forms.CharField()

#     # def clean_title(self):
#     #     cleaned_data = self.cleaned_data #dictionary
#     #     print("cleaned_data", cleaned_data)
#     #     title = cleaned_data.get('title')
#     #     if title.lower().strip() == "2":
#     #         raise forms.ValidationError("Title already exists")
#     #     print("title", title)
#     #     return title

#     def clean(self):
#         cleaned_data = self.cleaned_data
#         print("all data", cleaned_data)
#         title = cleaned_data.get('title')
#         content = cleaned_data.get('content')
#         if title.lower().strip() == "2":
#             self.add_error('title', 'This title is taken')
#             # raise forms.ValidationError("Title already exists")

#         if 'a' in content or 'a' in title.lower():
#             self.add_error('content', 'This content cannot be added')
#             raise forms.ValidationError('This is not allowed')

#         return cleaned_data
    
    

