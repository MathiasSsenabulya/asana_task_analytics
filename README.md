# asana_tasks_analytics

## Installation & Use Notes
* Install fresh python environment and activate it
* Install all program packages with: pip install -r requirements.txt
* Add into **"asana_task_analytics_project/secrets/"** directory following files:
    * secrets.py
    * Analytics Code-d9b5f2ff02e5.json
* Fill in secrets.py file with necessary credentials described in "secrets.py template" below.

###To use scalar metrics you should start django web server which will server as API service.
Simply run "python manage.py runserver 0.0.0.0:8000" command.
To obtain scalar metrics data request the following url "http://server_address:8000/api/scalar_metrics/top_latent/mit_or_miw_tag_id/"
where "server_address: is the domain or ip address of server and "mit_or_miw_tag_id" is the id of MIT/MIW tags created in Asana.
This endpoint should return json with top_latent data records filtered by oldest tasks.

###To obtain a series metrics:
Run "python manage.py series_metrics" command.
The program will obtain data from Asana API, analyse it and save output data into google spreadsheet. It appends a new row with today's data for each new day.
This command should be run frequently by cron.


###secrets.py template:
* ASANA_PERSONAL_ACCESS_TOKEN = 'some asana personal access token'
* ASANA_MIT_TAG_ID = "14423571806636"
* ASANA_MIW_TAG_ID = "14410378551182"
* ASANA_WORKSPACE_ID = "1968482998660"

###Analytics Code-d9b5f2ff02e5.json
Obtained from google drive api service