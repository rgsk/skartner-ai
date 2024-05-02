# Stop and remove existing MongoDB container if it exists
docker stop langchain-final-mongo
docker rm langchain-final-mongo

# Create a named Docker volume for MongoDB data persistence
docker volume rm langchain-final-mongo-data
