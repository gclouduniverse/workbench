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
