FROM nvidia/cuda:10.2-base-ubuntu18.04
CMD nvidia-smi

ENV WORKDIR /app
WORKDIR $WORKDIR

RUN apt-get update && \
    apt-get install -y \
    python3.7 \
    python3-pip \
    wget \
    git

COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install torch torchvision
#RUN pip3 install torch==1.7.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

ARG DOWNLOAD_MODEL_URL

RUN if [ ${DOWNLOAD_MODEL_URL} ]; then \
        python3 download_model.py ${DOWNLOAD_MODEL_URL}; \
    fi

ENTRYPOINT ["python3", "api.py"]
