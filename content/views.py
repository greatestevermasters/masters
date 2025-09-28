from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict
from .models import Content
from django.http import Http404
from .models import CONTENT_TYPE_CHOICES
from social.models import LikeDislike, Share, Comment

# ✅ added imports for login protection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# ---------- Home ----------
@login_required
def home(request):
    """
    Landing page: shows a quick preview of latest items
    across all masters and content types.
    """
    latest_items = Content.objects.order_by("-created")[:12]

    ct = ContentType.objects.get_for_model(Content)
    for obj in latest_items:
        obj.app_label = ct.app_label
        obj.model_name = ct.model

    items_by_type = defaultdict(list)
    for item in latest_items:
        items_by_type[item.content_type].append(item)

    content_types = [
        ("teaching", "Teachings"),
        ("book", "Books"),
        ("video", "Videos"),
        ("blog", "Blogs"),
    ]

    return render(
        request,
        "index.html",
        {
            "items": latest_items,
            "content_types": content_types,
            "items_by_type": dict(items_by_type),  # always a dict
        },
    )


# ---------- Master Home ----------
@login_required
def master_home(request, master):
    latest_items = Content.objects.filter(master=master).order_by("-created")

    # Ensure string keys matching the template
    items_by_type = {ctype: [] for ctype in ["teaching", "book", "video", "blog"]}
    for item in latest_items:
        # Use string keys to match template
        items_by_type[item.content_type].append(item)

    content_types = [
        ("teaching", "Teachings"),
        ("book", "Books"),
        ("video", "Videos"),
        ("blog", "Blogs"),
    ]

    ct = ContentType.objects.get_for_model(Content)
    highlighted_item = latest_items.first() if latest_items.exists() else None

    if highlighted_item:
        prev_item = Content.objects.filter(
            master=master,
            content_type=highlighted_item.content_type,
            id__lt=highlighted_item.id
        ).order_by('-id').first()

        next_item = Content.objects.filter(
            master=master,
            content_type=highlighted_item.content_type,
            id__gt=highlighted_item.id
        ).order_by('id').first()

        like_count = LikeDislike.objects.filter(content_type=ct, object_id=highlighted_item.id, value=1).count()
        dislike_count = LikeDislike.objects.filter(content_type=ct, object_id=highlighted_item.id, value=-1).count()
        share_count = Share.objects.filter(content_type=ct, object_id=highlighted_item.id).count()
        comments = Comment.objects.filter(content_type=ct, object_id=highlighted_item.id).order_by('-created')
    else:
        prev_item = next_item = None
        like_count = dislike_count = share_count = 0
        comments = []

    context = {
        "master": master,
        "items_by_type": items_by_type,  # now guaranteed to have string keys
        "content_types": content_types,
        "prev_item": prev_item,
        "next_item": next_item,
        "prev_url": prev_item.get_absolute_url() if prev_item else None,
        "next_url": next_item.get_absolute_url() if next_item else None,
        "highlighted_item": highlighted_item,
        "app_label": ct.app_label,
        "model_name": ct.model,
        "like_count": like_count,
        "dislike_count": dislike_count,
        "share_count": share_count,
        "comments": comments,
    }

    return render(request, "content/content_home.html", context)


# ---------- Global Type List ----------
@login_required
def global_type_list(request, content_type):
    """
    Show all items of a particular content type (teaching/book/video/blog)
    across all masters.
    """
    if content_type not in ["teaching", "book", "video", "blog"]:
        # fallback or 404
        raise Http404("Content type not found")

    items = Content.objects.filter(content_type=content_type).order_by("-created")

    content_types = [
        ('teaching', 'Teachings'),
        ('book', 'Books'),
        ('video', 'Videos'),
        ('blog', 'Blogs'),
    ]

    template_name = f"content/{content_type}_list.html"  # safe now

    context = {
        'items': items,
        'content_type': content_type,
        'content_types': content_types,
        'prev_url': request.META.get('HTTP_REFERER', '/'),
        'next_url': '',
    }

    return render(request, template_name, context)


# ---------- List View ----------
class ContentList(LoginRequiredMixin, ListView):
    """
    List page filtered by master and content_type.
    Examples:
        /buddha/teaching/
        /osho/book/
        /krishna/blog/
    """
    model = Content
    context_object_name = "items"

    def get_queryset(self):
        master = self.kwargs["master"]
        ctype = self.kwargs["content_type"]
        return Content.objects.filter(master=master, content_type=ctype).order_by("-created")

    def get_template_names(self):
        ctype = self.kwargs["content_type"]
        return [f"content/{ctype}_list.html"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["master"] = self.kwargs["master"]
        ctx["content_type"] = self.kwargs["content_type"]
        return ctx


# ---------- Detail View ----------
class ContentDetail(LoginRequiredMixin, DetailView):
    """
    Detail page for a single piece of content.
    Examples:
        /buddha/teaching/some-slug/
        /krishna/video/another-slug/
    """
    model = Content
    context_object_name = "item"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        master = self.kwargs["master"]
        ctype = self.kwargs["content_type"]
        return Content.objects.filter(master=master, content_type=ctype)

    def get_template_names(self):
        ctype = self.kwargs["content_type"]
        return [f"content/{ctype}_detail.html"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # App/model info for social buttons
        ct = ContentType.objects.get_for_model(Content)
        ctx["app_label"] = ct.app_label
        ctx["model_name"] = ct.model
        ctx["master"] = self.kwargs["master"]
        ctx["content_type"] = self.kwargs["content_type"]

        # Current item
        item = ctx["item"]

        # Previous / Next items
        prev_item = Content.objects.filter(
            master=ctx["master"],
            content_type=ctx["content_type"],
            id__lt=item.id
        ).order_by('-id').first()

        next_item = Content.objects.filter(
            master=ctx["master"],
            content_type=ctx["content_type"],
            id__gt=item.id
        ).order_by('id').first()

        ctx["prev_item"] = prev_item
        ctx["next_item"] = next_item
        ctx["prev_url"] = prev_item.get_absolute_url() if prev_item else None
        ctx["next_url"] = next_item.get_absolute_url() if next_item else None
        
        ctx["current_url"] = item.get_absolute_url()

        # --- Social button counts ---
        ctx["like_count"] = LikeDislike.objects.filter(content_type=ct, object_id=item.id, value=1).count()
        ctx["dislike_count"] = LikeDislike.objects.filter(content_type=ct, object_id=item.id, value=-1).count()
        ctx["share_count"] = Share.objects.filter(content_type=ct, object_id=item.id).count()
        ctx["comments"] = Comment.objects.filter(content_type=ct, object_id=item.id).order_by('-created')

        return ctx
