FROM python:3.5

# System
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    ca-certificates \
    postgresql-client \
    curl

RUN mkdir /application && \
    mkdir -p /root/.xonotic/repo_resources
WORKDIR /application

COPY xmra /application/xmra
COPY requirements.in /application/requirements.in

RUN pip install pip --upgrade && \
    pip install -r /application/requirements.in

COPY docker/containers/api/bin/wait-for-services.sh /application/wait-for-services.sh
RUN chmod +x /application/wait-for-services.sh

EXPOSE 8010