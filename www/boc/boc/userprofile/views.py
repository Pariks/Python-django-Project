from django.shortcuts import render
from userprofile.forms import PhoneForm, AvatarForm
from django.http import JsonResponse
from userprofile.models import UserExtraInfo
from django.http import HttpResponse, HttpResponseRedirect
from userprofile.models import UserProfile, UserFollowedBy
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Create your views here.
def phone_number(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST or None)
        if form.is_valid():
            phone_number = form.save(commit=False)
            if request.user.is_authenticated():
                phone_number.user = request.user
            phone_number.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse(form.errors, status=400)
def index(request):
    followed_by_count = UserFollowedBy.objects.filter(user=request.user).count()
    following_count = UserFollowedBy.objects.filter(followed_by=request.user).count()
    return render(request, 'userprofile/userprofile.html', {'following_count':following_count,
        'followed_by_count':followed_by_count})
def avatar_update(request):
    # Handle file upload
    if request.method == 'POST':                                                                                                                                                                                                                                                                                                            
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            userprofile = UserProfile.objects.filter(user=request.user)
            if userprofile:
                obj1 = UserProfile.objects.get(user=request.user)
                form = AvatarForm(request.POST, request.FILES, instance=obj1)
                form.save()
            else:
                avatar_form = form.save(commit=False)
                avatar_form.user = request.user
                avatar_form.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('userprofile:index'))
    else:
        form = AvatarForm() # A empty, unbound form
    return render(request,
        'userprofile/upload_avatar.html',
        {'form': form}
    )
def profile_display(request, username):
    user_info = User.objects.get(username=username)
    followed_by_count = UserFollowedBy.objects.filter(user__username=username).count()
    following_count = UserFollowedBy.objects.filter(followed_by=user_info).count()
    return render(request, 'userprofile/profile_display.html', {'user_info':user_info,
        'followed_by_count':followed_by_count, 'following_count':following_count})
def follow_user(request, username):
    followed_by = UserFollowedBy.objects.filter(user=request.user, followed_by__username=username)
    user_obj = User.objects.filter(username=username)
    if not followed_by and username != request.user.username and user_obj:
        user_obj = User.objects.get(username=username)
        followed_by_obj = UserFollowedBy(user=user_obj, followed_by=request.user)
        followed_by_obj.save()
    return HttpResponseRedirect(reverse('userprofile:index'))
