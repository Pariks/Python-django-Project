from django import forms
from userprofile.models import PhoneNumber, UserProfile
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions

class PhoneForm(forms.ModelForm):
    phone_number = forms.CharField(label=_("Phone Number"), min_length=6, max_length=50, widget=forms.TextInput(attrs={'placeholder': '(###) ###-####'}), required=True)
    
    class Meta:
        fields = ['phone_number']
        model = PhoneNumber
           
    def __init__(self, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs) 



class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        try:
            w, h = get_image_dimensions(avatar)
            #validate dimensions
            max_width = max_height = 300 
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))
            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG '
                    ' or PNG image.')
            #validate file size
            if len(avatar) > (1000 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')
        except AttributeError:
            """ 
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass
        return avatar
