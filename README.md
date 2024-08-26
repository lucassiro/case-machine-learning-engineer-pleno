Para rodar no Docker:
```
docker build -t fastapi-app .
docker run -p 8000:80 -d fastapi-app
```