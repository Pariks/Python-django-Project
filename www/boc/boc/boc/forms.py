from django import forms
from userprofile.models import UserExtraInfo
from followpost.models import Comments
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    news_letter = forms.BooleanField(required=False, label="I would like to receive occasional newsletters, offers and product updates from BetonCombat.com")
    
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        user_extras = UserExtraInfo(user=user, news_letter=self.cleaned_data['news_letter'])
        user_extras.save()
        print user_extras
        
        
class PostForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 100, 'placeholder': 'Add comments...', 'required':'true'}))
    class Meta:
        model = Comments
        fields = ('content',)
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)



class FlatPageForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={}))

    class Meta:
        model = FlatPage
        fields = '__all__'


class PageAdmin(FlatPageAdmin):
    """
    Page Admin
    """
    form = FlatPageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)        
