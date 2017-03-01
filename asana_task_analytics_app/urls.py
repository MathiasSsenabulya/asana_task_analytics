from django.conf.urls import url
import asana_task_analytics_app.views as views

urlpatterns = [
    url(r'api/scalar_metrics/mit/$', views.top_latent_mit_tasks, name='scalar_metrics_mit'),
    url(r'api/scalar_metrics/miw/$', views.top_latent_miw_tasks, name='scalar_metrics_miw'),
]
