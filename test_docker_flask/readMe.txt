To containerize the flask app run the following commands:
docker build -t flask-app .
docker run -p 5000:5000 -d flask-app
docker ps
docker exec -it 4f5843c43359 bash 
