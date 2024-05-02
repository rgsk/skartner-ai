# Stop and remove existing MongoDB container if it exists
docker stop langchain-final-mongo
docker rm langchain-final-mongo

# Create a named Docker volume for MongoDB data persistence
docker volume create langchain-final-mongo-data

# Run the MongoDB container as a replica set
docker run \
    -p 27020:27017 \
    --name langchain-final-mongo \
    -v langchain-final-mongo-data:/data/db \
    -d mongo:latest
