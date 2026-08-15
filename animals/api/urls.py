from django.urls import path
from animals.api.views import AnimalDetailView, AnimalListCreateView, RecordAccessGrantCreateView, RecordAccessGrantListView, RecordAccessGrantRevokeView, VeterinaryRecordDetailView, VeterinaryRecordListCreateView

urlpatterns = [
    path("animals/", AnimalListCreateView.as_view(), name="animal-list-create"),
    path("animals/<uuid:pk>/", AnimalDetailView.as_view(), name="animal-detail"),
    path("records/", VeterinaryRecordListCreateView.as_view(), name="record-list-create"),
    path("records/<uuid:pk>/", VeterinaryRecordDetailView.as_view(), name="record-detail"),
    path("record-grants/", RecordAccessGrantListView.as_view(), name="record-grant-list"),
    path("record-grants/create/", RecordAccessGrantCreateView.as_view(), name="record-grant-create"),
    path("record-grants/<uuid:pk>/revoke/", RecordAccessGrantRevokeView.as_view(), name="record-grant-revoke"),
]
