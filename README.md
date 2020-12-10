1  docker build --tag server .
2  docker run -it --name -p 8000:8000 -v "${pwd}":/app server_cont server