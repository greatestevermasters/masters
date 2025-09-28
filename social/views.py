from django.shortcuts import get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
from functools import wraps
from .models import Comment, LikeDislike, Share
from django.contrib.auth.decorators import login_required


#.....imports for news letter below......
from django.shortcuts import redirect
from django.contrib import messages
from .forms import NewsletterForm

def newsletter_subscribe(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for subscribing!")
        else:
            messages.error(request, "Invalid email or already subscribed.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


def ajax_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "message": "Please login first"}, status=401)
            else:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
        return func(request, *args, **kwargs)
    return wrapper

@ajax_login_required
def add_comment(request, app_label, model_name, object_id):
    if request.method == "POST":
        text = request.POST.get("text")
        model = ContentType.objects.get(app_label=app_label, model=model_name).model_class()
        obj = get_object_or_404(model, id=object_id)
        if text:
            comment = Comment.objects.create(user=request.user, content_object=obj, text=text)
            return JsonResponse({"success": True, "username": comment.user.username, "text": comment.text})
    return JsonResponse({"success": False})

@login_required

@login_required
@require_POST
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Ensure the user owns the comment
    if comment.user != request.user:
        return HttpResponseForbidden('You cannot edit this comment.')

    new_text = request.POST.get("text", "").strip()
    if not new_text:
        return JsonResponse({"success": False, "error": "Comment cannot be empty."})

    comment.text = new_text
    comment.save()
    return JsonResponse({"success": True, "text": comment.text})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == "POST":
        comment.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))


@ajax_login_required
def toggle_like(request, app_label, model_name, object_id, value):
    value = int(value)
    model = ContentType.objects.get(app_label=app_label, model=model_name).model_class()
    obj = get_object_or_404(model, id=object_id)
    like_obj, created = LikeDislike.objects.get_or_create(
        user=request.user,
        content_type=ContentType.objects.get_for_model(obj),
        object_id=obj.id,
        defaults={"value": value},
    )
    if not created:
        if like_obj.value == value:
            like_obj.delete()
        else:
            like_obj.value = value
            like_obj.save()
    like_count = LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, value=1).count()
    dislike_count = LikeDislike.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, value=-1).count()
    return JsonResponse({"success": True, "like_count": like_count, "dislike_count": dislike_count})

@ajax_login_required
def share_object(request, app_label, model_name, object_id, platform="link"):
    model = ContentType.objects.get(app_label=app_label, model=model_name).model_class()
    obj = get_object_or_404(model, id=object_id)
    Share.objects.create(user=request.user, content_object=obj, platform=platform)
    share_count = Share.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id).count()
    return JsonResponse({"success": True, "share_count": share_count})
