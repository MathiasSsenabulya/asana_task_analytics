import os
import json
from datetime import datetime

import asana
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from asana_task_analytics_project.secrets.secrets import *
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asana_task_analytics_project.settings")
django.setup()


class GoogleSpreadsheetHandler:
    def __init__(self):
        scope = [
            'https://spreadsheets.google.com/feeds',
            # 'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name('asana_task_analytics_project/secrets/Analytics Code-d9b5f2ff02e5.json', scope)
        gc = gspread.authorize(credentials)
        sh = gc.open('Asana Metrics')
        self.worksheet = sh.sheet1
        self.last_row_number = self.worksheet.row_count

    # Helpers
    def get_num_of_week_for_today(self):
        today = datetime.today()
        return today.strftime("%U")

    def create_new_row_for_today(self):
        """
           Cell names:
        A - Date
        B - Year-Week
        C - MIT Added
        D - MIT Completed
        E - MIT Average Age
        F - MIW Added
        G - MIW Completed
        H - MIW Average Age
        I - NIW Added
        J - NIW Completed
        K - NIW Average Age
        :return:
        """
        date_today = datetime.today().strftime("%m/%d/%Y")

        # If we don't have a row for today's date
        if self.worksheet.acell("A%d" % self.last_row_number).value != date_today:  # A3...n-cell
            # Then create a new row
            self.worksheet.append_row([
                date_today,
                "{}-{}".format(datetime.today().strftime("%Y"), self.get_num_of_week_for_today())
            ])
            self.last_row_number += 1

    def update_row_for_today(self, new_data_list):
        """
        Cell names:
        A - Date - shouldn't updated here!!!
        B - Year-Week - shouldn't updated here!!!
        C - MIT Added
        D - MIT Completed
        E - MIT Average Age
        F - MIW Added
        G - MIW Completed
        H - MIW Average Age
        I - NIW Added
        J - NIW Completed
        K - NIW Average Age

        :param new_data_list: [
        {'cell_label': 'C', 'value': 123},
        {'cell_label': 'D', 'value': 5},
        {'cell_label': 'E', 'value': 222}
        ]
        :return:
        """
        for data in new_data_list:
            print(data)
            cell_to_update = "{}{}".format(data["cell_label"], self.last_row_number)
            self.worksheet.update_acell(cell_to_update, data['value'])


class AsanaSeriesMetrics:
    """
    Extracts data from Asana API, calculates and returns outputs.

        Cell names for list_dicts_outputs:
        A - Date - shouldn't updated here!!!
        B - Year-Week - shouldn't updated here!!!
        C - MIT Added
        D - MIT Completed
        E - MIT Average Age
        F - MIW Added
        G - MIW Completed
        H - MIW Average Age
        I - NIW Added
        J - NIW Completed
        K - NIW Average Age
    """
    def __init__(self):
        self.client = asana.Client.access_token(MATVEY_ASANA_PERSONAL_ACCESS_TOKEN)
        self.output_new_data_list = []
        self.current_date = datetime.now().strftime('%Y-%m-%d')

        # me = self.client.users.me()
        # print(me['workspaces'])
        #
        # tags = self.client.tags.find_all({'workspace': MATVEY_ASANA_WORKSPACE_ID})
        # for tag in tags:
        #     print(tag)

    def get_tasks_by_tag_id(self, tag_id):
        """
        Performs tasks query with searched by ASANA_TAG_ID
        Mathias Ssenabulya
        Workspace_ID = 1968482998660
        [{'id': 14410378551182, 'name': 'Most Important This Week'},
        {'id': 14423571806636, 'name': 'Most Important Today'},
        {'id': 28211362476024, 'name': 'Next Important This Week'}]
        """
        # print(client.tags.find_all({'workspace': "1968482998660"}))
        tasks = self.client.tasks.find_all(
            {
                'tag': tag_id,
                'completed_since': self.current_date
            }
        )
        return tasks

    def get_task_history_by_task_id(self, task_id):
        task_history = self.client.tasks.stories(task_id)
        return task_history

    def get_task_date_added_to_tag_from_task_story(self, task_story):
        """
        Iterates over task history records and returns most recent date added to particular tag
        :param task_story:
        :return:
        """
        output = {}
        added_to_tag = None
        for history_record in task_story:
            if 'Most Important Today' in history_record['text']:
                if not added_to_tag:
                    added_to_tag = history_record['created_at']
                else:
                    if added_to_tag < history_record['created_at']:
                        added_to_tag = history_record['created_at']
                output = {'added_date': added_to_tag}
        return output

    # Asana API
    def mit_tasks_added_by_day(self):
        added_today_counter = 0
        # Return tasks either completed on\since current_date\today or all uncompleted tasks at all.
        tasks = self.get_tasks_by_tag_id(MATVEY_ASANA_MIT_TAG_ID)

        # Then we have to iterate over tasks and fetch task history.
        for task in tasks:
            task_history = self.get_task_history_by_task_id(task['id'])
            # Next we need analyse and find out at what date the task was added to MIT tag.
            task_added_date = self.get_task_date_added_to_tag_from_task_story(task_history)
            task_added_date = datetime.strptime(task_added_date['added_date'][:-5], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
            if task_added_date == self.current_date:
                added_today_counter += 1
        print(added_today_counter)
        return added_today_counter

    def mit_tasks_completed_by_day(self):
        task = self.client.tasks.find_by_id('285984735768128')
        print(json.dumps(task))

        pass

    def miw_tasks_added_by_day(self):
        pass

    def miw_tasks_completed_by_day(self):
        pass

    def mit_average_age_by_day(self):
        pass

    def miw_average_age_by_day(self):
        pass

    def get_data_from_asana_api_to_spreadsheet(self):
        """
        :return: self.output_new_data_list: [
        {'cell_label': 'C', 'value': 123},
        {'cell_label': 'D', 'value': 5},
        {'cell_label': 'E', 'value': 222}
        ]
        """
        # mit_tasks_added_by_day
        self.mit_tasks_added_by_day()


new_data_list = [
        {'cell_label': 'C', 'value': 123},
        {'cell_label': 'D', 'value': 5},
        {'cell_label': 'E', 'value': 222}
        ]

# Processing Google Spreadsheet
# spreadhseet_handler = GoogleSpreadsheetHandler()
# spreadhseet_handler.create_new_row_for_today()
# spreadhseet_handler.update_row_for_today(new_data_list)

# Processing Asana API
asana_series_metrics_handler = AsanaSeriesMetrics()
asana_series_metrics_handler.get_data_from_asana_api_to_spreadsheet()
