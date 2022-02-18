import argparse

from workbench.prediction.model_builder import create_model
from workbench.prediction.model_deployer import deploy_model
from workbench.executor import execute_local_notebook


def main():
    parser = argparse.ArgumentParser(prog="workbench",
                                     description="GCP Vertex AI Workbench CLI")
    parser.add_argument("action", choices=["build", "deploy", "execute-notebook"],
                                help="action")
    execute_notebook_group = parser.add_argument_group("execute-notebook")
    deployer_group.add_argument("--project", type=str, dest="project",
                                help="GCP Project (Vertex AI Workbench API should be enabled)")
    deployer_group.add_argument("--location", type=str, dest="location",
                                help="location should be supported by Vertex AI Workbench ")
    deployer_group.add_argument("--gcs-folder", type=str, dest="gcs_folder",
                                help="required for storing your notebook as well as the output")
    deployer_group.add_argument("--notebook", type=str, dest="notebook",
                                help="path for notebook to execute")
    deployer_group.add_argument("--vm-type", type=str, dest="vm_type",
                                help="type of VM to use for execution", default="n1-standard-4")
    deployer_group.add_argument("--env-container", type=str, dest="env_container",
                                help="Docker container, should be basead on GCP Deep Learnign Containers", 
                                default="gcr.io/deeplearning-platform-release/base-cu110:latest")
    deployer_group.add_argument("--kernel", type=str, dest="kernel",
                                help="kernels to use, your container should be compatible with this kernel", 
                                default="python3")
    deployer_group.add_argument("--execution-id", type=str, dest="execution_id",
                                help="execution id, should be unique or leave empty", 
                                default="")
    builder_group = parser.add_argument_group("build")
    builder_group.add_argument("--tag", type=str, dest="tag", required=True,
                                help="Docker Tag To Use With Build And/Or Deploy")
    builder_group.add_argument("--path", type=str, dest="path", default=".",
                                help="path to prediction.py file")
    deployer_group = parser.add_argument_group("deploy")
    deployer_group.add_argument("--tag", type=str, dest="tag", required=True,
                                help="Docker Tag To Use With Build And/Or Deploy")
    deployer_group.add_argument("--project", type=str, dest="project",
                                help="GCP Project (Vertex AI API should be enabled)")
    deployer_group.add_argument("--location", type=str, dest="location",
                                help="Vertex AI location")
    deployer_group.add_argument("--name", type=str, dest="name",
                                help="model name")

    args = parser.parse_args()

    if args.action == "build":
        create_model(args.tag, args.path)
    if args.action == "deploy":
        deploy_model(args.project, args.location, args.name, args.tag)
    if args.action == "execute-notebook":
        execute_local_notebook(args.project, 
                                args.location, 
                                args.notebook, 
                                args.gcs_folder, 
                                args.execution_id, 
                                args.env_container, 
                                args.kernel, 
                                args.vm_type)
