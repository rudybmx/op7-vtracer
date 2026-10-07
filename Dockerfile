FROM python:3.11-alpine

RUN apk add --no-cache libgcc

WORKDIR /app

COPY vtracer /usr/local/bin/vtracer
RUN chmod +x /usr/local/bin/vtracer

RUN pip install flask

COPY server.py .
COPY templates/ templates/
COPY static/ static/

EXPOSE 5000

CMD ["python3", "server.py"]
