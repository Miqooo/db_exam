
docker-compose down
docker image prune -f
docker-compose build api
docker-compose up