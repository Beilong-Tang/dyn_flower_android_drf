# Backend Server

## Set up

### Install the required dependencies

```sh
python3 -m pip install -r requirements.txt
```

### Run migrations

```sh
python3 manage.py migrate
```

### Download TFLite models

Download the models to `static/CIFAR10_model`.

The model files are at <https://www.dropbox.com/s/tubgpepk2q6xiny/models.zip?dl=1>.

Your `static/` should look like this:

```
 static
└──  CIFAR10_model
   ├──  bottleneck.tflite
   ├──  inference.tflite
   ├──  initialize.tflite
   ├──  optimizer.tflite
   └──  train_head.tflite
```

### Create TFLite model in database

Enter a Django shell:

```sh
python3 manage.py shell
```

Add the CIFAR10 model to database by:

```python
from train.models import *
m = TFLiteModel(name="CIFAR10_model", n_layers=10)
m.save()
f = TFLiteFile(path="/static/CIFAR10_model/bottleneck.tflite", tflite_model=m)
f.save()
f = TFLiteFile(path="/static/CIFAR10_model/inference.tflite", tflite_model=m)
f.save()
f = TFLiteFile(path="/static/CIFAR10_model/initialize.tflite", tflite_model=m)
f.save()
f = TFLiteFile(path="/static/CIFAR10_model/optimizer.tflite", tflite_model=m)
f.save()
f = TFLiteFile(path="/static/CIFAR10_model/train_head.tflite", tflite_model=m)
f.save()
```

Validate that the models are created:

```python
from train.serializers import *
s = TFLiteModelSerializer(m)
s.data
```

You should get:

```python
{'name': 'CIFAR10_model', 'n_layers': 10, 'tflite_files': ['/static/CIFAR10_model/bottleneck.tflite', '/static/CIFAR10_model/inference.tflite', '/static/CIFAR10_model/initialize.tflite', '/static/CIFAR10_model/optimizer.tflite', '/static/CIFAR10_model/train_head.tflite']}
```

## Development

To test on physical devices in development, run with

```sh
python3 manage.py runserver 0.0.0.0:8000
```

Find you local IP in your system settings for the physical device to connect to.


## Docker Deployment

This project can be deployed using Docker, which ensures that it will run the same way on every machine, regardless of the local setup.

### Pull the Docker Image

The Docker image for this project is hosted on Docker Hub. To pull the image to your local machine, run the following command:

```sh
docker pull fedcampus/dyn_flower_android_drf:initial
```

### Run the Docker Image

To run the Docker image, use the `docker run` command along with the appropriate port bindings. The application uses ports 8000 and 8080. Here's how you can run the Docker image:

```sh
docker run -p 8000:8000 -p 8080:8080 fedcampus/dyn_flower_android_drf:initial
```

This command maps port 8000 inside the Docker container to port 8000 on your host machine, and does the same for port 8080. 

### Testing with Docker

Once the Docker container is running, you can test the application by sending POST requests to the paths `/train/server` and `/train/get_advertised` on your localhost, using ports 8000 or 8080, depending on the service you're trying to reach. You can use curl or another tool to send these requests.

For example, to make a POST request to `/train/server` using curl, you would run the following command:

```sh
curl -X POST http://localhost:8000/train/server
```

And to make a POST request to `/train/get_advertised`, you would run:

```sh
curl -X POST http://localhost:8000/train/get_advertised
```

Remember to replace `localhost` and `8000` with the appropriate values if you're running Docker on a different host or port.
