from django.shortcuts import render
import custom_functions
import asana_task_analytics_project.settings as settings


def home(request):
    context = dict()
    context['tag_tasks'] = custom_functions.get_asana_tasks(settings.ASANA_TAG_ID)
    return render(request, 'asana_task_analytics/home.html', context)
