# JWT authentication with Django
My first JWT implementation project using django rest framework. JWT token can be fetched from http://localhost:8000/v0/authentications after starting the server.

## Usage
Run the server by starting the docker container. Container settings can be checked in [Dockerfile](./Dockerfile).

```bash
# build the container
Docker build -t jwt-django .

# run the container
Docker run -d --name jwt-django -p 8000:8000 jwt-django 
```