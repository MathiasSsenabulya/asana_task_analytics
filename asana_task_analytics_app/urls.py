from django.conf.urls import url
import asana_task_analytics_app.views as views

urlpatterns = [
    url(r'^$', views.home, name='asana_home'),
]
