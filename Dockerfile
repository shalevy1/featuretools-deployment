FROM platiagro/datascience-notebook
USER root
COPY . /app
WORKDIR /app
EXPOSE 5001

# Define environment variable
ENV MODEL_NAME Transform
ENV API_TYPE REST
ENV SERVICE_TYPE TRANSFORMER
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE --persistence $PERSISTENCE