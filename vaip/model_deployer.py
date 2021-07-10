from typing import Optional, Dict, Sequence, Tuple

from google.cloud import aiplatform


def deploy_model(project: str,
    location: str,
    display_name: str,
    serving_container_image_uri: str,):
    print("Uploading model")
    model = _upload_model(project, location, display_name, serving_container_image_uri)
    print(f"model: {model.resource_name}")
    print("Deploying model (this might take a LONG.... time)")
    _deploy_model(project, location, model.resource_name)


def _upload_model(
    project: str,
    location: str,
    display_name: str,
    serving_container_image_uri: str,
):

    aiplatform.init(project=project, location=location)

    model = aiplatform.Model.upload(
        display_name=display_name,
        serving_container_image_uri=serving_container_image_uri,
        serving_container_predict_route="/predict",
        serving_container_health_route="/ping",
        serving_container_ports=[8080],
        sync=True,
    )

    model.wait()

    print(model.display_name)
    print(model.resource_name)
    return model


def _deploy_model(
    project,
    location,
    model_name: str,
    endpoint: Optional[aiplatform.Endpoint] = None,
    deployed_model_display_name: Optional[str] = None,
):
    aiplatform.init(project=project, location=location)

    model = aiplatform.Model(model_name=model_name)

    model.deploy(
        endpoint=endpoint,
        deployed_model_display_name=deployed_model_display_name,
        traffic_percentage=100,
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=1,
        sync=True,
    )

    model.wait()

    print(model.display_name)
    print(model.resource_name)
    return model


# create_endpoint_sample("ml-lab-152505", "test-poc", "us-west1")
# projects/183488370666/locations/us-west1/endpoints/7882003035340144640
# upload_model_sample("ml-lab-152505", "us-west1", "test-poc", "us.gcr.io/ml-lab-152505/model-poc")
# projects/183488370666/locations/us-west1/models/2080170446635925504
# _deploy_model("ml-lab-152505", "us-west1", "projects/183488370666/locations/us-west1/models/2080170446635925504", deployed_model_display_name="test-poc")
# deploy_model("ml-lab-152505", "us-west1", "test-poc", "us.gcr.io/ml-lab-152505/model-poc")