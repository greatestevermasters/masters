from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    # Home page – shows global landing page
    path("", views.home, name="home"),  # /

    # Global content-type list (e.g. /type/teaching/)
    path("type/<str:content_type>/", views.global_type_list, name="global_type_list"),

    # Master home page (latest items for a specific master, e.g. /buddha/)
    path("<str:master>/", views.master_home, name="master_home"),

    # Content list for a specific master and type (e.g. /buddha/teaching/)
    path("<str:master>/<str:content_type>/", views.ContentList.as_view(), name="content_list"),

    # Detail page for an individual item (e.g. /buddha/teaching/some-slug/)
    path("<str:master>/<str:content_type>/<slug:slug>/", views.ContentDetail.as_view(), name="content_detail"),
]
