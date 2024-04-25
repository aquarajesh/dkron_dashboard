import requests
from datetime import datetime, timedelta,timezone
import json
from zoneinfo import ZoneInfo
# Define the dkron API endpoint
dkron_api_url = 'http://35.244.36.56:8080/v1'
# Retrieve list of job executions
response = requests.get(f'{dkron_api_url}/jobs')
timedelta_days = 7
def filter_jobs(response):
    executions = response.json()
    # Calculate threshold for identifying inactive jobs (e.g., 7 days ago)
    threshold = datetime.now(timezone.utc) - timedelta(days=timedelta_days)
    threshold = datetime.strptime(threshold.strftime('%Y-%m-%dT%H:%M:%SZ'),'%Y-%m-%dT%H:%M:%SZ')
    thresholdIST = datetime.now() - timedelta(days=timedelta_days)
    print("Threshold IST: %s" % thresholdIST)
    print("Threshold: %s UTC" % threshold.strftime('%Y-%m-%dT%H:%M:%SZ'))
    # List to store inactive job names
    inactive_jobs = []
    # Iterate over job executions to identify inactive jobs
    for execution in executions:
        job_id = execution['id']
        next_execution = datetime.strptime(execution['next'], '%Y-%m-%dT%H:%M:%SZ')
        # Check if job was executed before the threshold
        if next_execution < threshold:
           inactive_jobs.append({"id":job_id,"schedule":execution["schedule"],"nextschedule":execution['next']})
    # Display list of inactive jobs
    print("Inactive Jobs:")
    for inactive_job in inactive_jobs:
        print("-----deleting job:"+inactive_job["id"]+"-----")
        print("ScheduledAT:"+inactive_job['schedule']+":NextSchedule:"+inactive_job["nextschedule"])
        res = requests.delete(f'{dkron_api_url}/jobs/{inactive_job["id"]+"_test"}')
        if(res.status_code==200):
            print("Job successfully deleted")
        else:
            print("Job failed to delete")
            print(res.url)
        print("----------------------------------------------------------------")
if response.status_code == 200:
    try:
        data = response.json()
        filter_jobs(response)
    except json.JSONDecodeError:
        print("Error decoding JSON response")
else:
    print(f"HTTP request failed with status code: {response.status_code}")