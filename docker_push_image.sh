# Build the Image
docker build -t idep-delegation-sanford .

# Tag it 
docker tag idep-delegation-sanford:latest makalfe/idep-delegation-sanford:latest

# Push it
docker push makalfe/idep-delegation-sanford:latest