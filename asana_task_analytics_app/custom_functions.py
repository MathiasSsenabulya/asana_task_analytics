# -*- coding:utf-8 -*-
import asana
import asana_task_analytics_project.settings as settings

asana_api = asana.AsanaAPI(settings.ASANA_API_KEY, debug=True)


def get_asana_tasks(tag_id):
    """
    Performs tasks query with searched by ASANA_TAG_ID
    """
    tag_tasks = asana_api.get_tag_tasks(tag_id)
    return tag_tasks
