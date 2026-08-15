from django.urls import path
from disease.api.views import DiseaseAssessmentListCreateView

urlpatterns = [path("assessments/", DiseaseAssessmentListCreateView.as_view(), name="disease-assessment-list-create")]
