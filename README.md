# Accuknox

git clone to checkout the project

To install the web App to run it locally, you have to build the docker image first

Go to social_network/

Run the following command to build the docker image.

docker build -t social_network_project .

Then run the docker image

docker run -d -p 8080:8080 social_network_project

once it is started, you can hit the API to get started 

http://127.0.0.1:8080/api/signup/

Shared postman collection for each API endpoints on postman collections