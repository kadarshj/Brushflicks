from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from account.models import User
from .models import Artistshare, Hire, Gethired, Hirereq, Profile, UserSample, Sellart, SellProductAlbum
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )


class ArtistShareForm(forms.ModelForm):

    class Meta:
        model = Artistshare
        fields = ['art_type', 'created_by', 'description', 'cover_logo']

class HireForm(forms.ModelForm):
    skill_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Hire
        fields = ['hiring_skill', 'country', 'total_hour_work', 'budget', 'email_id', 'phone_no', 'cover_logo', 'skill_description']

class HireReqForm(forms.ModelForm):
    remark = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Hirereq
        fields = ['name', 'country', 'email_id', 'phone_no', 'profession', 'remark']

class GetHireForm(forms.ModelForm):
    personal_details = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Gethired
        fields = ['my_skill', 'country', 'hourly_charge', 'email_id', 'phone_no', 'cover_logo','personal_details']

class GetHireReqForm(forms.ModelForm):
    remark = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Hirereq
        fields = ['name', 'country', 'email_id', 'phone_no', 'remark']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields =['first_name','last_name','i_like_being','my_pic']

class PhotoForm(forms.ModelForm):
    sample_file = forms.FileField(label='Photo Album')

    class Meta:
        model = UserSample
        fields = ['sample_file']

class PaintImageForm(forms.ModelForm):
    sample_file = forms.FileField(label='Painting Image Album')

    class Meta:
        model = UserSample
        fields = ['sample_file']

class MusicForm(forms.ModelForm):
    sample_file = forms.FileField(label='Music Sample')

    class Meta:
        model = UserSample
        fields = ['sample_file']

class BandMusicForm(forms.ModelForm):
    sample_file = forms.FileField(label='Band Music Sample')

    class Meta:
        model = UserSample
        fields = ['sample_file']

class BlogForm(forms.ModelForm):
    sample_blog = forms.CharField(widget=forms.Textarea,label= 'Blog Sample')

    class Meta:
        model = UserSample
        fields = ['blog_name','sample_blog']

class SellArtForm(forms.ModelForm):

    class Meta:
        model = Sellart
        fields = ['seller_name', 'art_type', 'created_by', 'description', 'total_count_product', 'price', 'discount_price', 'seller_email_id', 'seller_phone_number', 'seller_delivery_charge', 'art_cover_logo']


class SellProductAlbumForm(forms.ModelForm):

    class Meta:
        model = SellProductAlbum
        fields = ['album_files']