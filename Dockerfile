FROM python:3.11-slim

WORKDIR /app
COPY src/static ./static

EXPOSE 8000
CMD ["python", "-m", "http.server", "8000", "--directory", "static"]
