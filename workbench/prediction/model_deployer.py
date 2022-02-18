from typing import Optional, Dict, Sequence, Tuple

from google.cloud import aiplatform

import yaml


def deploy_model(project: str,
    location: str,
    display_name: str,
    serving_container_image_uri: str,):
    print("Uploading model")
    model = _upload_model(project, location, display_name, serving_container_image_uri)
    print(f"model: {model.resource_name}")
    print("Deploying model (this might take a LONG.... time)")
    _deploy_model(project, location, model.resource_name)


def deploy_model_with_confg(
    display_name: str,
    serving_container_image_uri: str,
    config_path: str,):
    with open(config_path, "r") as f:
        config = yaml.load(f)
    print("Uploading model")
    model = _upload_model(
        config["project"], config["location"], 
        display_name, serving_container_image_uri)
    print(f"model: {model.resource_name}")
    print("Deploying model (this might take a LONG.... time)")
    _deploy_model_with_config(model.resource_name, config_path)



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


def _deploy_model_with_config(model_name: str, config) -> aiplatform.Model:
    config["model_name"] = model_name
    model = _deploy_model(**config)

    return model


def _deploy_model(
    project,
    location,
    model_name: str,
    endpoint: Optional[aiplatform.Endpoint] = None,
    deployed_model_display_name: Optional[str] = None,
    traffic_percentage: Optional[int] = 100,
    traffic_split: Optional[Dict[str, int]] = None,
    machine_type: Optional[str] = "n1-standard-2",
    min_replica_count: int = 1,
    max_replica_count: int = 1,
    accelerator_type: Optional[str] = None,
    accelerator_count: Optional[int] = None,
    service_account: Optional[str] = None,
    explanation_metadata = None,
    explanation_parameters = None,
    metadata: Optional[Sequence[Tuple[str, str]]] = (),
    encryption_spec_key_name: Optional[str] = None,
):
    aiplatform.init(project=project, location=location)

    model = aiplatform.Model(model_name=model_name)

    model.deploy(
        endpoint=endpoint,
        deployed_model_display_name=deployed_model_display_name,
        traffic_percentage=traffic_percentage,
        traffic_split=traffic_split,
        machine_type=machine_type,
        min_replica_count=min_replica_count,
        max_replica_count=max_replica_count,
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
        service_account=service_account,
        explanation_metadata=explanation_metadata,
        explanation_parameters=explanation_parameters,
        metadata=metadata,
        encryption_spec_key_name=encryption_spec_key_name,
        sync=True,
    )

    model.wait()

    print(model.display_name)
    print(model.resource_name)
    return model
