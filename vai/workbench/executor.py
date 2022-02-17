import urllib

import google.auth.transport.requests
import google.oauth2.id_token
import uuid


def execute_notebook(gcp_project: str, 
                     location: str, 
                     gcs_input_notebook_file_path: str, 
                     gcs_output_notebook_folder_path: str, 
                     execution_id="", 
                     env_uri="gcr.io/deeplearning-platform-release/base-cu110:latest", 
                     kernel="python3", 
                     master_type="n1-standard-4"):
    if not execution_id:
        execution_id = str(uuid.uuid1())

    service_url = f"https://notebooks.googleapis.com/v1/projects/{gcp_project}/locations/{location}/executions?execution_id={execution_id}"
    values = {
        "description": f"Execution for {gcs_input_notebook_file_path}",
        "executionTemplate": {
            "scaleTier": "CUSTOM",
            "masterType": master_type,
            "inputNotebookFile": gcs_input_notebook_file_path,
            "outputNotebookFolder": gcs_output_notebook_folder_path,
            "containerImageUri": env_uri,
            "kernelSpec": kernel
        }
    }
    data = urllib.parse.urlencode(values).encode('ascii')
    print(f"url to call: {service_url}")
    print(f"data to send: {data}")
    creds, _ = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    req = urllib.request.Request(service_url, data=data, headers={
                "Content-Type": "application/json"
            })
    req.add_header("Authorization", f"Bearer {creds.token}")
    response = urllib.request.urlopen(req)

    return response.read()

if "__main__" == __name__:
    # https://notebooks.googleapis.com/v1/projects/ml-lab-152505/locations/us-central1/executions?execution_id=3a5c9802-8f8d-11ec-b585-acde48001122
    # https://notebooks.googleapis.com/v1/projects/ml-lab-152505/locations/us-central1/executions?execution_id=0e05f924-8f8d-11ec-9223-acde48001122
    # :path: /aipn/v2/proxy/notebooks.googleapis.com%2Fv1%2Fprojects%2Fml-lab-152505%2Flocations%2Fus-central1%2Fexecutions%3Fexecution_id%3Duntitled__1645052627007?1645052645915
    # URL: https://7cc62a62987d13d7-dot-us-central1.notebooks.googleusercontent.com/aipn/v2/proxy/notebooks.googleapis.com%2Fv1%2Fprojects%2Fml-lab-152505%2Flocations%2Fus-central1%2Fexecutions%3Fexecution_id%3Duntitled__1645052627007?1645052645915
    print(execute_notebook("ml-lab-152505", "us-central1", "gs://test-bucket-for-notebooks/executor_files/untitled__1645052627007/Untitled.ipynb", "gs://test-bucket-for-notebooks/executor_files/untitled__1645052627007", execution_id="untitiled123"))