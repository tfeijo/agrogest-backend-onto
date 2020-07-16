FROM python:3.8

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

# Install Java.
RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive \
apt-get -y install default-jre-headless && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

CMD ["python", "app.py"]