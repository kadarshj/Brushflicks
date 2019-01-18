from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.views import View
from account.models import User
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import Artistshare, Artliked, Artflagged, Hire, Gethired, Profile, UserSample, Sellart, SellProductAlbum
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic.edit import UpdateView
from .forms import SignUpForm,ArtistShareForm, HireForm, HireReqForm, GetHireForm, ProfileForm, PhotoForm, PaintImageForm, BandMusicForm, BlogForm, MusicForm, GetHireReqForm, SellArtForm, SellProductAlbumForm
from .tokens import account_activation_token
#import datetime
import hashlib
from django.core.urlresolvers import reverse
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
import uuid

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
# Create your views here.
@login_required
def home(request):
    #artsharelist = Artistshare.objects.all()
    artshare_list = Artistshare.objects.order_by('-date')
    user = request.user
    user_obj = User.objects.get(email = user)
    user_id = user_obj.id

    page = request.GET.get('page', 1)
    paginator = Paginator(artshare_list, 50)
    try:
        artsharelist = paginator.page(page)
    except PageNotAnInteger:
        artsharelist = paginator.page(1)
    except EmptyPage:
        artsharelist = paginator.page(paginator.num_pages)

    return render(request,"account/home.html",{'artsharelist': artsharelist, 'user_id': user_id})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account/account_activation_invalid.html')

@login_required
def creativetype(request):
    return render(request, 'account/creativetype.html')

@login_required
def art_share(request):
    form = ArtistShareForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        artshare = form.save(commit=False)
        artshare.user = request.user
        artshare.cover_logo = request.FILES['cover_logo']
        file_type = artshare.cover_logo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'artshare': artshare,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'account/share_art.html', context)
        artshare.save()
        #return render(request, 'account/detail.html', {'artshare': artshare})
        return redirect('home')
    context = {
        "form": form,
    }
    return render(request, 'account/share_art.html', context)


@login_required
def art_liked(request,art_post_id,user_id):
    #artlike = get_object_or_404(Artliked,user_id = user_id,art_id=art_post_id)
    #artlike = Artliked.objects.get(user_id=user_id, art_id=art_post_id)

    artlike = Artliked.objects.filter(user_id=user_id, art_id=art_post_id).first()
    if not artlike:
        Artliked.objects.create(user_id=user_id, art_id=art_post_id)
    else:
       # Artliked.delete()
       #  try:
        if artlike.is_liked:
            artlike.is_liked = False
        else:
            artlike.is_liked = True
            #artlike.user_id = user_id
            #artlike.art_id = art_post_id
        artlike.save()
        #art_obj = Artistshare.objects.get(pk = art_post_id)
        art_obj = get_object_or_404(Artistshare,pk=art_post_id)
        count = Artliked.objects.filter(art_id=art_post_id,is_liked=True).count()
        art_obj.like_count = count
        art_obj.save()
        like = '#'+'like'+str(art_post_id)
   # except (KeyError, artlike.DoesNotExist):
    if not artlike:
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True, 'count': count, 'like': like})

@login_required
def art_flagged(request,art_post_id,user_id):
    artflag = Artflagged.objects.filter(user_id=user_id, art_id=art_post_id).first()
    if not artflag:
        Artflagged.objects.create(user_id=user_id, art_id=art_post_id)
    else:
        # Artliked.delete()
        #  try:
        if artflag.is_flag_liked:
            artflag.is_flag_liked = False
        else:
            artflag.is_flag_liked = True
            # artlike.user_id = user_id
            # artlike.art_id = art_post_id
        artflag.save()
        #art_obj = Artistshare.objects.get(pk=art_post_id)
        art_obj = get_object_or_404(Artistshare,pk=art_post_id)
        count = Artflagged.objects.filter(art_id=art_post_id, is_flag_liked=True).count()
        art_obj.flag_count = count
        art_obj.save()
        flag = '#' + 'flag' + str(art_post_id)
        # except (KeyError, artlike.DoesNotExist):
    if not artflag:
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True, 'count': count, 'flag': flag})



@login_required
def hire(request):
    form = HireForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        hire = form.save(commit=False)
        hire.user = request.user
        hire.cover_logo = request.FILES['cover_logo']
        file_type = hire.cover_logo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'hire': hire,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'account/hire.html', context)
        hire.save()
        # return render(request, 'account/detail.html', {'artshare': artshare})
        return redirect('hirehome')
    context = {
        "form": form,
    }
    return render(request, 'account/hire.html', context)

@login_required
def hirehome(request):
    #artsharelist = Artistshare.objects.all()
    hire_list = Hire.objects.order_by('-hire_post_created')
    user = request.user
    user_obj = User.objects.get(email = user)
    user_id = user_obj.id

    page = request.GET.get('page', 1)
    paginator = Paginator(hire_list, 50)
    try:
        hirelist = paginator.page(page)
    except PageNotAnInteger:
        hirelist = paginator.page(1)
    except EmptyPage:
        hirelist = paginator.page(paginator.num_pages)

    return render(request,"account/hire_home.html",{'hirelist': hirelist, 'user_id': user_id})


@login_required
def hiredetailreq(request):
    hire_post_id = request.POST.get('hire_post_id')
    user_id = request.POST.get('user_id')
    #hire_obj = Hire.objects.get(pk=hire_post_id)
    hire_obj = get_object_or_404(Hire,pk=hire_post_id)
    count_view = hire_obj.count_view + 1
    hire_obj.count_view = count_view
    form = HireReqForm(request.POST or None)
    if form.is_valid():
        hire_post_id = request.POST['hire_post_id']
        user_id = request.POST['user_id']
        hire_object = get_object_or_404(Hire,pk=hire_post_id)
        count_apply = hire_object.count_apply +1
        hire_object.count_apply = count_apply
        email_hire_id = hire_object.email_id

        hire_object.save()

        hirereq = form.save(commit=False)
        hirereq.hire_id = hire_post_id
        hirereq.user_id = user_id
        #hire.cover_logo = request.FILES['cover_logo']
        hirereq.save()

        name = request.POST['name']
        email_id = request.POST['email_id']
        country = request.POST['country']
        profession = request.POST['profession']
        #phone_no = request.POST['phone_no']
        remark = request.POST['remark']
        count_v = request.POST['count_view']
        date = request.POST['date']

        msg_html = render_to_string('account/emailtemp.html',
                                    {'name': name, 'email_id': email_id, 'country': country, 'profession': profession, 'count_v': count_v, 'date': date, 'count_apply': count_apply, 'remark': remark})

        send_mail(
            'Email From Interested Candidate By Brushflicks',
            'Thanks for email',
            'noreply@gmail.com',
            [email_hire_id],
            html_message=msg_html,
        )
        return redirect('emailsent')
    context = {
        "form": form,
        'hire_obj': hire_obj,
        'hire_post_id': hire_post_id,
        'user_id': int(user_id),
        'count_view': count_view
    }
    hire_obj.save()
    return render(request, 'account/hiredetail.html', context)


@login_required
def emailsent(request):
    return render(request, "account/emailsent.html")


@login_required
def gethire(request):
    form = GetHireForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        gethire = form.save(commit=False)
        gethire.user = request.user
        gethire.cover_logo = request.FILES['cover_logo']
        file_type = gethire.cover_logo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'gethire': gethire,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'account/gethire.html', context)
        gethire.save()
        # return render(request, 'account/detail.html', {'artshare': artshare})
        return redirect('gethirehome')
    context = {
        "form": form,
    }
    return render(request, 'account/gethire.html', context)


@login_required
def gethirehome(request):
    #artsharelist = Artistshare.objects.all()
    gethire_list = Gethired.objects.order_by('-gethire_post_created')
    user = request.user
    user_obj = User.objects.get(email = user)
    user_id = user_obj.id

    page = request.GET.get('page', 1)
    paginator = Paginator(gethire_list, 50)
    try:
        gethirelist = paginator.page(page)
    except PageNotAnInteger:
        gethirelist = paginator.page(1)
    except EmptyPage:
        gethirelist = paginator.page(paginator.num_pages)

    return render(request,"account/gethire_home.html",{'gethirelist': gethirelist, 'user_id': user_id})


@login_required
def gethiredetailreq(request):
    gethire_post_id = request.POST.get('gethire_post_id')
    user_id = request.POST.get('user_id')
    #hire_obj = Hire.objects.get(pk=hire_post_id)
    gethire_obj = get_object_or_404(Gethired,pk=gethire_post_id)
    count_view = gethire_obj.count_view + 1
    gethire_obj.count_view = count_view
    form = GetHireReqForm(request.POST or None)
    if form.is_valid():
        gethire_post_id = request.POST['gethire_post_id']
        user_id = request.POST['user_id']
        gethire_object = get_object_or_404(Gethired,pk=gethire_post_id)
        count_interest = gethire_object.count_interest +1
        gethire_object.count_interest = count_interest
        email_gethire_id = gethire_object.email_id

        gethire_object.save()

        gethirereq = form.save(commit=False)
        gethirereq.hire_id = gethire_post_id
        gethirereq.user_id = user_id
        #hire.cover_logo = request.FILES['cover_logo']
        gethirereq.save()

        name = request.POST['name']
        email_id = request.POST['email_id']
        country = request.POST['country']
        #phone_no = request.POST['phone_no']
        remark = request.POST['remark']
        count_v = request.POST['count_view']
        date = request.POST['date']

        msg_html = render_to_string('account/emailtotemp.html',
                                    {'name': name, 'email_id': email_id, 'country': country, 'count_v': count_v, 'date': date, 'count_interest': count_interest, 'remark': remark})

        send_mail(
            'Email From Interested Candidate By Brushflicks',
            'Thanks for email',
            'noreply@gmail.com',
            [email_gethire_id],
            html_message=msg_html,
        )
        return redirect('emailtosent')
    context = {
        "form": form,
        'gethire_obj': gethire_obj,
        'gethire_post_id': gethire_post_id,
        'user_id': int(user_id),
        'count_view': count_view
    }
    gethire_obj.save()
    return render(request, 'account/gethiredetail.html', context)

@login_required
def emailtosent(request):
    return render(request, "account/emailtosent.html")

@login_required
def profileupdate(request):
    user_id = request.POST.get('user_id')
    instance = get_object_or_404(Profile, user_id=user_id)
    form = ProfileForm(instance=instance)
    if request.method == "POST":
      profileform = ProfileForm(request.POST or None, instance=instance)
      if profileform.is_valid():
        instance = profileform.save(commit=False)
        #instance.my_pic = request.FILES['my_pic']
        instance.my_pic = request.FILES.get('my_pic', False)
        if instance.my_pic == False:
            context = {
                'instance': instance,
                'form': form,
                'error_message': 'Please select my pic file!',
                'user_id': user_id,
            }
            return render(request, 'account/profile_form.html', context)
        file_type = instance.my_pic.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'instance': instance,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
                'user_id': user_id,
            }
            return render(request, 'account/profile_form.html', context)
        instance.save()
        if instance.i_like_being == 'painter':
         return render(request, 'account/upload_sample.html', {'instance': instance})
        elif instance.i_like_being == 'musician':
         return render(request, 'account/upload_sample_music.html', {'instance': instance})
        elif instance.i_like_being == 'band':
         return render(request, 'account/upload_sample_band.html', {'instance': instance})
        elif instance.i_like_being == 'photography':
         return render(request, 'account/upload_sample_photography.html', {'instance': instance})
        else:
         return render(request, 'account/upload_sample_blogger.html', {'instance': instance})
    context = {"instance": instance, "form": form, 'user_id': user_id}
    return render(request, 'account/profile_form.html', context)


@login_required
def postpainterimg(request):
        form = PaintImageForm(request.POST, request.FILES)
        if form.is_valid():
            photoform = form.save(commit=False)
            user = request.user
            user_obj = User.objects.get(email=user)
            user_id = user_obj.id
            photoform.user_id = int(user_id)
            photoform.is_painter = True
            photo = photoform.save()
            #usersample = UserSample.objects.filter(user_id = user_id, is_painter= True)
            return render(request, 'account/done.html', {'success': True})

        context = {'form': form}
        return render(request, 'account/done.html', context)

@login_required
def postmusic(request):
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            musicform = form.save(commit=False)
            user = request.user
            user_obj = User.objects.get(email=user)
            user_id = user_obj.id
            musicform.user_id = int(user_id)
            musicform.is_musician = True
            photo = musicform.save()
            #usersample = UserSample.objects.filter(user_id = user_id, is_painter= True)
            return render(request, 'account/done.html', {'success': True})

        context = {'form': form}
        return render(request, 'account/done.html', context)

@login_required
def postphoto(request):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photoform = form.save(commit=False)
            user = request.user
            user_obj = User.objects.get(email=user)
            user_id = user_obj.id
            photoform.user_id = int(user_id)
            photoform.is_photgraphy = True
            photo = photoform.save()
            #usersample = UserSample.objects.filter(user_id = user_id, is_painter= True)
            return render(request, 'account/done.html', {'success': True})

        context = {'form': form}
        return render(request, 'account/done.html', context)


@login_required
def postbandmusic(request):
        form = BandMusicForm(request.POST, request.FILES)
        if form.is_valid():
            musicform = form.save(commit=False)
            user = request.user
            user_obj = User.objects.get(email=user)
            user_id = user_obj.id
            musicform.user_id = int(user_id)
            musicform.is_band = True
            photo = musicform.save()
            #usersample = UserSample.objects.filter(user_id = user_id, is_painter= True)
            return render(request, 'account/done.html', {'success': True})

        context = {'form': form}
        return render(request, 'account/done.html', context)


@login_required
def postblog(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        blogform = form.save(commit=False)
        user = request.user
        user_obj = User.objects.get(email=user)
        user_id = user_obj.id
        blogform.user_id = int(user_id)
        blogform.is_blog = True

        blogform.save()
        # return render(request, 'account/detail.html', {'artshare': artshare})
        return redirect('home')
    context = {
        "form": form,
    }
    return render(request, 'account/upload_sample_blogger.html', context)


@login_required
def profiledetails(request):
    user_id = request.POST.get('user_id')
    profile = get_object_or_404(Profile, user_id=user_id)

    user_paintpiclist = UserSample.objects.filter(user_id=user_id, is_painter= True)
    user_piclist = UserSample.objects.filter(user_id=user_id,is_photography= True)
    user_musiclist = UserSample.objects.filter(user_id=user_id, is_musician= True)
    user_bandlist = UserSample.objects.filter(user_id=user_id, is_band= True)
    user_bloglist = UserSample.objects.filter(user_id=user_id, is_blog= True)

    return render(request, "account/profile.html", {'profile': profile, 'user_id': user_id, 'user_paintpiclist': user_paintpiclist, 'user_piclist': user_piclist, 'user_musiclist': user_musiclist, 'user_bandlist': user_bandlist, 'user_bloglist': user_bloglist})


@login_required
def artsavedcard(request):
    user = request.user
    user_obj = User.objects.get(email=user)
    user_id = user_obj.id

    #list = Artliked.objects.filter(user_id = user_id, is_liked = True)
    liked_list = Artflagged.objects.select_related('art').filter(user_id = user_id, is_flag_liked=True).order_by('-flag_created')


    page = request.GET.get('page', 1)
    paginator = Paginator(liked_list, 50)
    try:
        artlikedlist = paginator.page(page)
    except PageNotAnInteger:
        artlikedlist = paginator.page(1)
    except EmptyPage:
        artlikedlist = paginator.page(paginator.num_pages)

    return render(request, "account/savedcard.html", {'artlikedlist': artlikedlist, 'user_id': user_id})


def saveddelete(request):
    user_id = request.POST.get('user_id')
    art_id = request.POST.get('art_id')

    unflag = get_object_or_404(Artflagged, user_id=user_id, art_id= art_id)
    unflag.is_flag_liked = False
    unflag.save()
    return redirect('savedcard')


@login_required
def sellartshare(request):
    form = SellArtForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        artsell = form.save(commit=False)
        artsell.user = request.user
        artsell.art_cover_logo = request.FILES['art_cover_logo']
        file_type = artsell.art_cover_logo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'artsell': artsell,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'account/sell_art.html', context)
        artsell_list = artsell.save()
        new_obj = Sellart.objects.get(id=artsell.id)
        return render(request, 'account/product_sell_album.html', {'new_obj': new_obj})
        #return redirect('')
    context = {
        "form": form,
    }
    return render(request, 'account/sell_art.html', context)


@login_required
def PostProductAlbum(request):
        form = SellProductAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            photoform = form.save(commit=False)
            user = request.user
            user_obj = User.objects.get(email=user)
            user_id = user_obj.id
            photoform.user_id = int(user_id)
            sell_id = request.POST.get('sell_id')
            photoform.sell_id = sell_id
            photo = photoform.save()
            #usersample = UserSample.objects.filter(user_id = user_id, is_painter= True)
            return render(request, 'account/done.html', {'success': True})

        context = {'form': form}
        return render(request, 'account/done.html', context)


@login_required
def sellhome(request):
    #artsharelist = Artistshare.objects.all()
    artshare_list = Sellart.objects.order_by('-date')
    user = request.user
    user_obj = User.objects.get(email = user)
    user_id = user_obj.id

    page = request.GET.get('page', 1)
    paginator = Paginator(artshare_list, 50)
    try:
        artsharelist = paginator.page(page)
    except PageNotAnInteger:
        artsharelist = paginator.page(1)
    except EmptyPage:
        artsharelist = paginator.page(paginator.num_pages)

    return render(request,"account/Sell_Art_Home.html",{'artsharelist': artsharelist, 'user_id': user_id})


@login_required
def kart(request):
   return render(request, 'account/kartdata.html', {})

@login_required
def payment(request):
    amount = request.POST.get('amount')
    shipping_name = request.POST.get('shipping_name')
    shipping_street_address = request.POST.get('shipping_street_address')
    shipping_country = request.POST.get('shipping_country')
    shipping_state = request.POST.get('shipping_state')
    shipping_city = request.POST.get('shipping_city')
    shipping_pincode = request.POST.get('shipping_pincode')
    shipping_mobile = request.POST.get('shipping_mobile')
    shipping_email = request.POST.get('shipping_email')
    artsell_id = request.POST.getlist('artsell_id')
    quantity = request.POST.getlist('quantity')

    MERCHANT_KEY = "gtKFFx"
    key = "gtKFFx"
    SALT = "eCwWELxi"
    PAYU_BASE_URL = "https://test.payu.in/_payment"
    action = ''
    posted = {}
    for i in request.POST:
        posted[i] = request.POST[i]
    #hash_object = hashlib.sha256(b'randint(0,20)')
    #txnid = hash_object.hexdigest()[0:20]
    txnid = str(uuid.uuid1().int >> 64)
    hashh = ''
    posted['txnid'] = txnid
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key'] = key
    posted['surl'] = request.build_absolute_uri(reverse("success"))
    posted['furl'] = request.build_absolute_uri(reverse("failure"))
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(posted[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += SALT
    hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    action = PAYU_BASE_URL
    if (posted.get("key") != None and posted.get("txnid") != None and posted.get("productinfo") != None and posted.get("firstname") != None and posted.get("email") != None):
        return render(request,'account/payment.html', {"posted": posted, "hashh": hashh,"MERCHANT_KEY": MERCHANT_KEY,"txnid": txnid,"hash_string": hash_string,"action": "https://test.payu.in/_payment"})
    else:
        return render(request,'account/payment.html', {"posted": posted, "hashh": hashh,"MERCHANT_KEY": MERCHANT_KEY,"txnid": txnid,"hash_string": hash_string,"action": "."})



@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "eCwWELxi"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
    return render_to_response(request, 'brushflicks/account/success.html', {"txnid": txnid, "status": status, "amount": amount})






@csrf_protect
@csrf_exempt
def failure(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "eCwWELxi"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
    return render_to_response(request, "account/failure.html", c)


@login_required
def sellartdetail(request):
    sell_post_id = request.POST["sell_post_id"]
    user_id = request.POST["user_id"]

    prod_list = get_object_or_404(Sellart, pk=sell_post_id)
    photo_list = SellProductAlbum.objects.filter(user_id=user_id, sell_id=sell_post_id)
    #unflag = get_object_or_404(Artflagged, user_id=user_id, art_id=art_id)

    sell_obj = get_object_or_404(Sellart, pk=sell_post_id)
    count_view = sell_obj.count_view + 1
    sell_obj.count_view = count_view
    sell_obj.save()

    return render(request, 'account/sell_art_details.html', {'prod_list':prod_list,'photo_list':photo_list })


@login_required
def contact(request):
   return render(request, 'account/contact.html', {})

@login_required
def symbol(request):
   return render(request, 'account/symbol.html', {})












