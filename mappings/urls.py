from django.urls import path

from .views import MappingDetailView, MappingListCreateView

urlpatterns = [
    path("", MappingListCreateView.as_view(), name="mapping_list_create"),
    path("<int:pk>/", MappingDetailView.as_view(), name="mapping_detail"),
]
