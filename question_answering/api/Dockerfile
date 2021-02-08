FROM ubuntu:18.04

ENV WORKDIR /app
WORKDIR $WORKDIR

RUN apt-get update && \
    apt-get install -y \
    python3.7 \
    python3-pip \
    wget \
    git

# Install "software-properties-common" (for the "add-apt-repository")
RUN apt-get update && apt-get install -y \
    software-properties-common

RUN rm -rf /var/lib/apt/lists/*

COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

ARG DOWNLOAD_MODEL

RUN if [ ${DOWNLOAD_MODEL} ]; then \
        python3.6 download_model.py ${DOWNLOAD_MODEL}; \
    fi

CMD python3 api.py