import argparse

from workbench.prediction.model_builder import create_model
from workbench.prediction.model_deployer import deploy_model
from workbench.executor import execute_local_notebook
from workbench.prediction.notebook_model_builder import create_model

import warnings

def main():
    warnings.filterwarnings("ignore")

    parser = argparse.ArgumentParser(prog="workbench",
                                     description="GCP Vertex AI Workbench CLI")
    parser.add_argument("action", choices=["build", "deploy", "execute-notebook", "extract-model-from-notebook"],
                                help="action")
    parser.add_argument("--tag", type=str, dest="tag", required=False,
                                help="Docker Tag To Use With Build And/Or Deploy")


    execute_notebook_group = parser.add_argument_group("execute-notebook")
    execute_notebook_group.add_argument("--gcs-folder", type=str, dest="gcs_folder",
                                help="required for storing your notebook as well as the output")
    execute_notebook_group.add_argument("--notebook", type=str, dest="notebook",
                                help="path for notebook to execute")
    execute_notebook_group.add_argument("--vm-type", type=str, dest="vm_type",
                                help="type of VM to use for execution", default="n1-standard-4")
    execute_notebook_group.add_argument("--env-container", type=str, dest="env_container",
                                help="Docker container, should be basead on GCP Deep Learnign Containers", 
                                default="gcr.io/deeplearning-platform-release/base-cu110:latest")
    execute_notebook_group.add_argument("--kernel", type=str, dest="kernel",
                                help="kernels to use, your container should be compatible with this kernel", 
                                default="python3")
    execute_notebook_group.add_argument("--execution-id", type=str, dest="execution_id",
                                help="execution id, should be unique or leave empty", 
                                default="")
    execute_notebook_group.add_argument("--wait", action='store_true', dest="wait",
                                help="wait until exeuction is finished", default=False)
    location_argument = execute_notebook_group.add_argument("--location", type=str, dest="location",
                                help="location should be supported by Vertex AI Workbench ")
    project_argument = execute_notebook_group.add_argument("--project", type=str, dest="project",
                                help="GCP Project (Vertex AI API should be enabled)")

    extract_model_notebook_group = parser.add_argument_group("extract-model-from-notebook")
    extract_model_notebook_group.add_argument("--src", type=str, dest="src",
                                help="root of the source folder, will be copied to the container")
    extract_model_notebook_group.add_argument("--main-notebook", type=str, dest="main_nb",
                                help="main notebook, from where to extract the prediction logic")
    extract_model_notebook_group.add_argument("--target", type=str, dest="target", default=None,
                                help="taget folder for generated Dockerfile and files around")
    extract_model_notebook_group.add_argument("--generate-only", action='store_true', dest="generate_only", default=False,
                                help="will not build/push docker, only generate Dockerfile and files")

    builder_group = parser.add_argument_group("build")
    builder_group.add_argument("--path", type=str, dest="path", default=".",
                                help="path to prediction.py file")
    deployer_group = parser.add_argument_group("deploy")
    deployer_group.add_argument("--name", type=str, dest="name",
                                help="model name")
    deployer_group._group_actions.append(location_argument)
    deployer_group._group_actions.append(project_argument)

    args = parser.parse_args()

    if args.action == "build":
        create_model(args.tag, args.path)
    elif args.action == "deploy":
        deploy_model(args.project, args.location, args.name, args.tag)
    elif args.action == "execute-notebook":
        result = execute_local_notebook(args.project, 
                                args.location, 
                                args.notebook, 
                                args.gcs_folder, 
                                args.execution_id, 
                                args.env_container, 
                                args.kernel, 
                                args.vm_type,
                                args.wait)
        if not result:
            print("Execution failed")
        else:
            print("Result will be visible at: " + result["viewer_url"])
            print("Executed notebook will be at: " + result["notebook_gcs_url"])
            print("Execution id: " + result["execution_uri"])
            print("Operation id: " + result["operation_uri"])
    elif args.action == "extract-model-from-notebook":
        create_model(args.tag, args.src, args.main_nb, args.target, args.generate_only)
    else:
        print("ERROR, incorrect action")

if __name__ == "__main__":
    main()
