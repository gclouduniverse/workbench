import os
import shutil
from typing import Optional
from vaip import constants

import docker
import tempfile


def create_model(tag: str,
                 src_folder: Optional[str] = "."):
    with tempfile.TemporaryDirectory() as tmpdir:
        target_dir = os.path.join(
            tmpdir, constants.TEMP_DIR_FOR_BUILDING_CONTAINERS)
        print("Preparing Docker env")
        _check_if_prediction_file_exist(src_folder)
        print("Preparing Docker env")
        _move_docker_content_to_temp_dir(target_dir)
        print("Moving content of the current dir to the temp location")
        shutil.copytree(src_folder, target_dir, dirs_exist_ok=True)
        print("Building and pushing docker container")
        _build_and_push_docker(target_dir, tag)
        print("done")


def _check_if_prediction_file_exist(target_dir):
    prediction_file = os.path.join(target_dir, constants.MAIN_PREDICTION_FILE)
    if not os.path.isfile(prediction_file):
        raise ValueError(
            "The prediction file {} does not exist".format(prediction_file))


def _move_docker_content_to_temp_dir(target_dir):
    src = os.path.join(
        os.path.dirname(__file__), constants.PACKAGE_DIR_FOR_CONTAINER)
    shutil.copytree(src, target_dir, dirs_exist_ok=True)


def _build_and_push_docker(path, tag):
    client = docker.from_env()
    client.images.build(path=path, tag=tag)
    client.images.push(tag)


# create_model("us.gcr.io/ml-lab-152505/model-poc", main_nb_name="test.ipynb")
# create_model()
