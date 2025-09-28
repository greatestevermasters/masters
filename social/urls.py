from django.urls import path
from . import views

urlpatterns = [
    path("toggle_like/<str:app_label>/<str:model_name>/<int:object_id>/<str:value>/", views.toggle_like, name="toggle_like"),
    path("add_comment/<str:app_label>/<str:model_name>/<int:object_id>/", views.add_comment, name="add_comment"),
    path("comment/<int:pk>/edit/", views.edit_comment, name="edit_comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    path("share/<str:app_label>/<str:model_name>/<int:object_id>/<str:platform>/", views.share_object, name="share_object"),
    path("subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
]
