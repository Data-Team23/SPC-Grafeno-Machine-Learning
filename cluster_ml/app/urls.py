from django.urls import path
from .views import (
    RFMDataView,
    PreprocessedRFMView,
    ClusteredDataView,
    ClusterCentersView,
    ClusterMetricsView,
)

urlpatterns = [
    path('rfm/', RFMDataView.as_view(), name='rfm_data'),
    path('preprocessed/', PreprocessedRFMView.as_view(), name='preprocessed_rfm'),
    path('clusters/', ClusteredDataView.as_view(), name='clustered_data'),
    path('centers/', ClusterCentersView.as_view(), name='cluster_centers'),
    path('metrics/', ClusterMetricsView.as_view(), name='cluster_metrics'),
]
