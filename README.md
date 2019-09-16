# Featuretools Deployment

[![docker pulls](https://img.shields.io/docker/pulls/platiagro/featuretools-deployment.svg)](https://hub.docker.com/r/platiagro/featuretools-deployment/)
[![docker stars](https://img.shields.io/docker/stars/platiagro/featuretools-deployment.svg)](https://hub.docker.com/r/platiagro/featuretools-deployment/)
[![image metadata](https://images.microbadger.com/badges/image/platiagro/featuretools-deployment.svg)](https://microbadger.com/images/platiagro/featuretools-deployment "platiagro/featuretools-deployment image metadata")
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Gitter](https://badges.gitter.im/platiagro/community.svg)](https://gitter.im/platiagro/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## Building the Docker image

In the project directory, run:

```shell
docker build -t platiagro/featuretools-deployment:0.0.1 .
```

## Deploying a Docker container

After building the image, run:

```shell
docker run --rm -it -p 5000:5000 -e EXPERIMENT_ID=autofeaturing-automl/fruits -e BUCKET=mlpipeline -e TARGET=price_alvo -e DATE=DATA -e DATE_FORMAT=%Y-%m-%d -e GROUP=Item_Name platiagro/featuretools-deployment:0.0.1
```

## Usage

```shell
curl -X POST localhost:5000/transform-input -d 'json={"data":{"ndarray":[[67,82,291,1,1,1041,846,334,706,1086,256,1295,766,968,1185,1355,1842,90,"Operator1","2016-01-01","2016-01-01"]],"names":["Temperature","Humidity","Measure1","Measure2","Measure3","Measure4","Measure5","Measure6","Measure7","Measure8","Measure9","Measure10","Measure11","Measure12","Measure13","Measure14","Measure15","Hours Since Previous Failure","Operator","Date","DT"]}}'
```