# scheduler-server

# Use ubuntu base image
FROM ubuntu:22.04

WORKDIR /app

# Ensure we're set to UTC
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install python
RUN apt-get update && apt-get install -y python3 \
    python3-pip \
    git

# Install dumb-init
RUN pip install dumb-init

# Copy in and install requirements
# This will leverage the cache for rebuilds when modifying the code, avoiding
# downloading all the requirements again
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Install schedlib
COPY . .
RUN pip install .

# Run server
EXPOSE 8010
ENTRYPOINT ["dumb-init", "gunicorn", "--bind", "0.0.0.0:8010", "--timeout", "180", "scheduler_server.app:app"]
