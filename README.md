# Vertex AI Workbench High Level SDK

Install it:

```bash
pip install ai-workbnech
```

Only python >= 3.8 is currently supported.

## Executing Notebooks

Submit local notebook to execution:

```bash
workbench execute-notebook --notebook ./notebooks/clean.ipynb --gcs-folder gs://gtc-conf-examples/ --location us-central1 --project ml-lab-152505
```

## Deploy To Prediction

This SDK/CLI makes it very-very simple to deploy your Python logic to Vertex AI Prediction. In fact you just need to do two things:

* write python prediction function
* name file that stores python prediction function ```prediction.py```

your prediction function must comply with the following interface:

```python
def predict(instance, **kwarg):
    pass
```

Workbench has to main actions:
* build (creates Docker image with your logic that is fully compatible with Vertex Prediction)
* deploy (cloud be done with as easily with ```gcloud```) - deploys container from the step #1 to the Vertex predciton

During the build stage, under the hood VIAP will do:
* it will create Docker container with Flask
* it will correctly configure Flask to recognize your funciton ```predict```
* it will copy all the files from the current folder to the container
* it will install all python requirenments from the ```requirenmnets.txt``` file

### Test Yourself

Do not belive my word. Install CLI:

```bash
pip install ai-workbnech
```

go to the ```demo``` directory and run the following command:

```bash
TAG=... # your tag that you can push somewhere, e.g."us.gcr.io/ml-lab-152505/model-poc"
workbnech build --tag "${TAG}" --path .
```

test it, start container locally:

```bash
TAG=... # your tag that you can push somewhere, e.g."us.gcr.io/ml-lab-152505/model-poc"
docker run -p 8080:8080 "${TAG}"
```

run the prediction:
```bash
curl -X POST -d '{"parameters": {}, "instances": ["1", "2"]}' -H "Content-Type: application/json" http://localhost:8080/predict
```

you should see:

```
{"predictions":["Hello Vertex","Hello Vertex"]}
```