from django.shortcuts import render
import asana_task_analytics_project.settings as settings

import asana

client = asana.Client.access_token(settings.ASANA_PERSONAL_ACCESS_TOKEN)


# Helpers
def get_asana_tasks(tag_id):
    """
    Performs tasks query with searched by ASANA_TAG_ID
    Mathias Ssenabulya
    Workspace_ID = 1968482998660
    {'id': 14410378551182, 'name': 'Most Important This Week'}
    {'id': 14423571806636, 'name': 'Most Important Today'}
    {'id': 28211362476024, 'name': 'Next Important This Week'}
    """
    # print(client.tags.find_all({'workspace': "1968482998660"}))
    tasks = client.tasks.find_all({'tag': "14423571806636"}, item_limit=20)
    return tasks


# Endpoints
def home(request):
    context = dict()
    context['tag_tasks'] = get_asana_tasks(settings.ASANA_TAG_ID)
    return render(request, 'asana_task_analytics/home.html', context)
