import argparse

from vaip.model_builder import create_model
from vaip.model_deployer import deploy_model


def main():
    parser = argparse.ArgumentParser(prog="vaip",
                                     description="GCP Vertex AI Model Publisher")
    parser.add_argument("--tag", type=str, dest="tag", required=True,
                                help="Docker Tag To Use With Build And/Or Deploy")
    parser.add_argument("action", choices=["build", "deploy"],
                                help="action")
    builder_group = parser.add_argument_group("build")
    builder_group.add_argument("--path", type=str, dest="path", default=".",
                                help="path to prediction.py file")
    deployer_group = parser.add_argument_group("deploy")
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