# Budowanie obrazu Docker
docker build . -t ner-api

# Opcjonalnie: Wypchnij obraz Docker do rejestru (np. Docker Hub)
docker tag ner-api:latest docker-images-registry.rcl2.local:9090/ner-api:latest
docker login docker-images-registry.rcl2.local:9090 -u aklos -p Warszawa12345!
docker push docker-images-registry.rcl2.local:9090/ner-api:latest