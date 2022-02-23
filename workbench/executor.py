import urllib
import json

import google.auth.transport.requests
import google.oauth2.id_token
import uuid
import time

from google.cloud import storage


def execute_local_notebook(gcp_project: str, 
                            location: str, 
                            input_notebook_file_path: str, 
                            gcs_notebook_folder_path: str, 
                            execution_id="", 
                            env_uri="gcr.io/deeplearning-platform-release/base-cu110:latest", 
                            kernel="python3", 
                            master_type="n1-standard-4",
                            wait=True):
    gcs_bucket_name = _get_gcs_bucket_name_from_gcs_uri(gcs_notebook_folder_path)
    file_name = input_notebook_file_path.split("/")[-1]
    gcs_out_path = "/".join(gcs_notebook_folder_path.replace("gs://", "").split("/")[1:]) + "/" + file_name
    input_gcs_notebook_path = f"gs://{gcs_notebook_folder_path}/{file_name}"
    _upload_blob(gcp_project, gcs_bucket_name, input_notebook_file_path, gcs_out_path)
    return execute_notebook(gcp_project, location, input_gcs_notebook_path, gcs_notebook_folder_path, execution_id, env_uri, kernel, master_type, wait)


def execute_notebook(gcp_project: str, 
                     location: str, 
                     gcs_input_notebook_file_path: str, 
                     gcs_output_notebook_folder_path: str, 
                     execution_id="", 
                     env_uri="gcr.io/deeplearning-platform-release/base-cu110:latest", 
                     kernel="python3", 
                     master_type="n1-standard-4",
                     wait=True):
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
    data = json.dumps(values).encode('utf-8')
    data_from_gcp = _send_generic_request(service_url, data)
    if not data_from_gcp:
        return None
    operation_uri = data_from_gcp["name"]
    execution_uri = data_from_gcp["metadata"]["target"]
    notebook_gcs_url = get_output_notebook_path(execution_uri)
    notebook_gcs_url_without_scheme = notebook_gcs_url.replace("gs://", "")
    viewer_url = f"https://notebooks.cloud.google.com/view/{notebook_gcs_url_without_scheme}"
    if not wait:
        return {
            "operation_uri": operation_uri,
            "execution_uri": execution_uri,
            "notebook_gcs_url": notebook_gcs_url,
            "viewer_url": viewer_url
        }
    else:
        execution_status = _wait_execution_to_complete(execution_uri)
        return {
            "operation_uri": operation_uri,
            "execution_uri": execution_uri,
            "notebook_gcs_url": notebook_gcs_url,
            "viewer_url": viewer_url,
            "execution_status": execution_status
        }


def get_output_notebook_path(execution_uri: str) -> str:
    reuqest_url = f"https://notebooks.googleapis.com/v1/{execution_uri}"
    response = _send_generic_request(reuqest_url)
    return response["outputNotebookFile"]


def _get_notebook_execution_operation_status(execution_uri: str):
    service_url = f"https://notebooks.googleapis.com/v1/{execution_uri}"
    data_from_gcp = _send_generic_request(service_url)
    # print(str(data_from_gcp))
    if "state" in data_from_gcp:
        return data_from_gcp["state"]
    elif "response" in data_from_gcp:
        return data_from_gcp["response"]["state"]
    else:
        return None


def _upload_blob(gcp_project, bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def _wait_execution_to_complete(execution_uri):
    execution_status = "IN_PROGRESS"
    while (execution_status != "DONE" and execution_status != "FAILED" and execution_status != "COMPLETED" 
                and execution_status != "FINISHED" and execution_status != "SUCCEEDED"):
            execution_status = _get_notebook_execution_operation_status(execution_uri)
            print(f"Execution status: {execution_status}")
            time.sleep(10) # Sleep for 10 seconds
    return execution_status


def _get_gcs_bucket_name_from_gcs_uri(gcs_uri):
    return gcs_uri.split("/")[2]


def _send_generic_request(url, data=None):
    creds, _ = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    req = urllib.request.Request(url, data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header("Authorization", f"Bearer {creds.token}")
    response = urllib.request.urlopen(req)
    if response.status != 200:
        print(f"Error: {response.status}")
        print(f"Error: {response.read()}")
        return None
    encoding = response.info().get_content_charset('utf-8')
    return json.loads(response.read().decode(encoding))


# if "__main__" == __name__:
#     print(_wait_execution_to_complete("projects/ml-lab-152505/locations/us-central1/executions/bb55aab0-94ca-11ec-a020-0242c0a80a02"))
#     print(_get_notebook_execution_operation_status("projects/ml-lab-152505/locations/us-central1/executions/58662e0e-9446-11ec-a214-0242c0a80a02"))
    # https://notebooks.googleapis.com/v1/projects/ml-lab-152505/locations/us-central1/executions?execution_id=3a5c9802-8f8d-11ec-b585-acde48001122
    # https://notebooks.googleapis.com/v1/projects/ml-lab-152505/locations/us-central1/executions?execution_id=0e05f924-8f8d-11ec-9223-acde48001122
    # :path: /aipn/v2/proxy/notebooks.googleapis.com%2Fv1%2Fprojects%2Fml-lab-152505%2Flocations%2Fus-central1%2Fexecutions%3Fexecution_id%3Duntitled__1645052627007?1645052645915
    # URL: https://7cc62a62987d13d7-dot-us-central1.notebooks.googleusercontent.com/aipn/v2/proxy/notebooks.googleapis.com%2Fv1%2Fprojects%2Fml-lab-152505%2Flocations%2Fus-central1%2Fexecutions%3Fexecution_id%3Duntitled__1645052627007?1645052645915
    # print(str(execute_notebook("ml-lab-152505", "us-central1", "gs://test-bucket-for-notebooks/executor_files/untitled__1645052627007/Untitled.ipynb", "gs://test-bucket-for-notebooks/executor_files/untitled__1645052627007", wait=True)))
    # notebook_gcs_url = get_output_notebook_path("projects/ml-lab-152505/locations/us-central1/executions/83214dfe-90d1-11ec-bd9d-acde48001122")
    # notebook_gcs_url_without_scheme = notebook_gcs_url.replace("gs://", "")
    # viewer_url = f"https://notebooks.cloud.google.com/view/{notebook_gcs_url_without_scheme}"
    # print(viewer_url)
    # print(execute_local_notebook("ml-lab-152505", "us-central1", "/Users/vsk/src/notebooks-ci-showcase/notebooks/clean.ipynb", "gs://test-bucket-for-notebooks/executor_files/"))
