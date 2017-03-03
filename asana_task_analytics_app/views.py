from operator import itemgetter

from django.shortcuts import render
from django.http import JsonResponse

import asana_task_analytics_project.settings as settings

import asana

client = asana.Client.access_token(settings.ASANA_PERSONAL_ACCESS_TOKEN)


class BaseMitAndMiW:
    def __init__(self, item_limit, tag_id):
        self.item_limit = item_limit
        self.tag_name = self.get_tag_name_by_id(tag_id)
        self.tag_id = tag_id

    def get_tag_name_by_id(self, tag_id):
        tags = client.tags.find_all({'workspace': "1968482998660"})
        for tag in tags:
            if tag['id'] == int(tag_id):
                return tag['name']

    def get_tasks_by_tag_id(self, tag_id, item_limit):
        """
        Performs tasks query with searched by ASANA_TAG_ID
        Mathias Ssenabulya
        Workspace_ID = 1968482998660
        [{'id': 14410378551182, 'name': 'Most Important This Week'},
        {'id': 14423571806636, 'name': 'Most Important Today'},
        {'id': 28211362476024, 'name': 'Next Important This Week'}]
        """
        # print(client.tags.find_all({'workspace': "1968482998660"}))
        tasks = client.tasks.find_all({'tag': tag_id, 'completed_since': 'now'}, item_limit=item_limit)
        return tasks

    def get_task_history_by_task_id(self, task_id):
        task_history = client.tasks.stories(task_id)
        return task_history


class AsanaTopTalentHandler(BaseMitAndMiW):
    def get_date_task_added_to_tag_from_task_story(self, task_stories_list_dicts):
        output = {}
        added_to_tag = None
        for history_record in task_stories_list_dicts:
            if self.tag_name in history_record['text']:
                if not added_to_tag:
                    added_to_tag = history_record['created_at']
                else:
                    if added_to_tag < history_record['created_at']:
                        added_to_tag = history_record['created_at']
                output = {'added_date': added_to_tag}
        return output

    def get_top_latent(self):
        """
        Scalar Metrics
        Top n Latent in TAG_NAME: Incomplete tasks with oldest date/time added to TAG_NAME
        Find all tasks with tag TAG_NAME
        :return:
        """
        top_latent = list()
        tasks = self.get_tasks_by_tag_id(self.tag_id, self.item_limit)
        for task in tasks:
            stories = list(self.get_task_history_by_task_id(task['id']))
            task_info_output = {'task_id': task['id'], 'task_title': task['name']}
            date_added = self.get_date_task_added_to_tag_from_task_story(stories)
            task_info_output.update(date_added)
            top_latent.append(task_info_output)

            print(task)
            print(stories)
            print("")

        rows_by_added_to = sorted(top_latent, key=itemgetter('added_date'))
        return rows_by_added_to


# /api/scalar_metrics/top_latent/(?P<tag_id>[0-9])
def get_top_latent_tasks(request, **kwargs):
    item_limit = None
    tag_id = kwargs.get("tag_id")
    try:
        top_latent_handler = AsanaTopTalentHandler(item_limit, tag_id)
        output = top_latent_handler.get_top_latent()
        return JsonResponse(output, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)})
