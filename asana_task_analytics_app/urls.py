from django.conf.urls import url
import asana_task_analytics_app.views as views

urlpatterns = [
    url(r'api/scalar_metrics/top_latent/(?P<tag_id>[0-9]{14})/$', views.get_top_latent_tasks, name='top_latent_tasks'),
]
