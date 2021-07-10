# Vertex AI Prediction (VAIP) High Level SDK

This SDK makes it very-very simple to deploy your Python logic to Vertex AI Prediction. In fact you just need to do two things:

* write python prediction function
* name file that stores python prediction function ```prediction.py```

your prediction function must comply with the following interface:

```python
def predict(instance, **kwarg):
    pass
```

VAIP has to main actions:
* build (creates Docker image with your logic that is fully compatible with Vertex Prediction)
* deploy (cloud be done with as easily with ```gcloud```) - deploys container from the step #1 to the Vertex predciton

During the build stage, under the hood VIAP will do:
* it will create Docker container with Flask
* it will correctly configure Flask to recognize your funciton ```predict```
* it will copy all the files from the current folder to the container
* it will install all python requirenments from the ```requirenmnets.txt``` file

# Test Yourself

Do not belive my word. Install CLI:

```python
pip install vaip
```

go to the test directory and run the following command:

```bash
TAG=... # your tag that you can push somewhere, e.g."us.gcr.io/ml-lab-152505/model-poc"
vaip build --tag "${TAG}" --path .
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