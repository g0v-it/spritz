VER=$1
docker build --build-arg version=$VER -t copernico-spritz:$VER .
docker push copernicani/copernico-spritz:$VER
