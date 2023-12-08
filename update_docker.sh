
CONTAINER_NAME=$(docker-compose ps -q api)

LOCAL_APP_PATH="./api/app"

if [ -z "$CONTAINER_NAME" ]; then
    echo "Container name not found. Skipping file copy and restart."
    docker start api
    CONTAINER_NAME=$(docker-compose ps -q api)
fi

CONTAINER_NAME=$(docker inspect --format '{{.Name}}' $CONTAINER_NAME | cut -d'/' -f2)
	
docker cp $LOCAL_APP_PATH/. $CONTAINER_NAME:/code/app
docker restart $CONTAINER_NAME
