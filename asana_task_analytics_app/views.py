from operator import itemgetter

from django.shortcuts import render
from django.http import JsonResponse

import asana_task_analytics_project.settings as settings

import asana

client = asana.Client.access_token(settings.ASANA_PERSONAL_ACCESS_TOKEN)


class BaseMitAndMiW:
    def __init__(self, item_limit):
        self.item_limit = item_limit

    def get_tasks_by_tag_id(self, tag_id, item_limit):
        """
        Performs tasks query with searched by ASANA_TAG_ID
        Mathias Ssenabulya
        Workspace_ID = 1968482998660
        {'id': 14410378551182, 'name': 'Most Important This Week'}
        {'id': 14423571806636, 'name': 'Most Important Today'}
        {'id': 28211362476024, 'name': 'Next Important This Week'}
        """
        # print(client.tags.find_all({'workspace': "1968482998660"}))
        tasks = client.tasks.find_all({'tag': tag_id}, item_limit=item_limit)
        return tasks

    def get_task_history_by_task_id(self, task_id):
        task_history = client.tasks.stories(task_id)
        return task_history


class AsanaMitHandler(BaseMitAndMiW):
    def check_completness_and_mit_from_task_stories(self, task_stories_list_dicts):
        added_to_mit = False
        completed_this_task = False
        for history_record in task_stories_list_dicts:
            if history_record['text'] == 'added to Most Important Today':
                added_to_mit = True
            elif history_record['text'] == 'removed from Most Important Today':
                added_to_mit = False
            elif history_record['text'] == 'completed this task':
                completed_this_task = True
        if added_to_mit and not completed_this_task:
            return False
        elif added_to_mit and completed_this_task:
            return True

    def get_date_task_added_to_mit_from_task_story(self, task_stories_list_dicts):
        output = {}
        added_to_mit = None
        for history_record in task_stories_list_dicts:
            if history_record['text'] == 'added to Most Important Today':
                if not added_to_mit:
                    added_to_mit = history_record['created_at']
                else:
                    if added_to_mit < history_record['created_at']:
                        added_to_mit = history_record['created_at']
                output = {'added_to_mit': added_to_mit}
        return output

    def get_top_latent_mit(self):
        """
        Scalar Metrics
        Top n Latent MIT: Incomplete MIT tasks with oldest date/time added to MIT
        Find all tasks with tag “Most Important Today”
        :return:
        """
        top_latent_mit = list()
        tasks = self.get_tasks_by_tag_id(settings.ASANA_TAG_ID, self.item_limit)
        for task in tasks:
            stories = list(self.get_task_history_by_task_id(task['id']))
            task_completed = self.check_completness_and_mit_from_task_stories(stories)
            if not task_completed:
                task_info_output = {'task_id': task['id'], 'task_title': task['name']}
                date_added_to_mit = self.get_date_task_added_to_mit_from_task_story(stories)
                task_info_output.update(date_added_to_mit)
                top_latent_mit.append(task_info_output)

                # print(task)
                # print(stories)
                # print("")

        rows_by_added_to_mit = sorted(top_latent_mit, key=itemgetter('added_to_mit'))
        return rows_by_added_to_mit


class AsanaMiwHandler(BaseMitAndMiW):
    def check_completness_and_miw_from_task_stories(self, task_stories_list_dicts):
        added_to_miw = False
        completed_this_task = False
        for history_record in task_stories_list_dicts:
            if history_record['text'] == 'added to Most Important This Week':
                added_to_miw = True
            elif history_record['text'] == 'completed this task':
                completed_this_task = True
            elif history_record['text'] == 'removed from Most Important This Week':
                added_to_miw = False
        if added_to_miw and not completed_this_task:
            return False
        elif added_to_miw and completed_this_task:
            return True

    def get_date_task_added_to_miw_from_task_story(self, task_stories_list_dicts):
        output = {}
        added_to_miw = None
        for history_record in task_stories_list_dicts:
            if history_record['text'] == 'added to Most Important This Week':
                if not added_to_miw:
                    added_to_miw = history_record['created_at']
                else:
                    if added_to_miw < history_record['created_at']:
                        added_to_miw = history_record['created_at']
                output = {'added_to_miw': added_to_miw}
        return output

    def get_top_latent_miw(self):
        """
        Scalar Metrics
        Top n Latent MIW: Incomplete MIW tasks with oldest date/time added to MIW
        Find all tasks with tag “Most Important This Week”
        :return:
        """
        top_latent_miw = list()
        tasks = self.get_tasks_by_tag_id(settings.ASANA_TAG_ID, self.item_limit)
        for task in tasks:
            stories = list(self.get_task_history_by_task_id(task['id']))
            task_completed = self.check_completness_and_miw_from_task_stories(stories)
            if not task_completed:
                task_info_output = {'task_id': task['id'], 'task_title': task['name']}
                date_added_to_miw = self.get_date_task_added_to_miw_from_task_story(stories)
                task_info_output.update(date_added_to_miw)
                top_latent_miw.append(task_info_output)

                # print(task)
                # print(stories)
                # print("")

        rows_by_added_to_miw = sorted(top_latent_miw, key=itemgetter('added_to_miw'))
        return rows_by_added_to_miw


# /api/scalar_metrics/mit/
def top_latent_mit_tasks(request):
    item_limit = 20
    mit_handler = AsanaMitHandler(item_limit)
    output = mit_handler.get_top_latent_mit()
    return JsonResponse(output, safe=False)


# /api/scalar_metrics/miw/
def top_latent_miw_tasks(request):
    item_limit = 20
    miw_handler = AsanaMiwHandler(item_limit)
    output = miw_handler.get_top_latent_miw()
    return JsonResponse(output, safe=False)
