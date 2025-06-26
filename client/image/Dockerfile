FROM nvcr.io/nvidia/tensorflow:24.06-tf2-py3

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt-get install -y cron bash
RUN apt-get install -y ffmpeg libsm6 libxext6
RUN apt-get install -y libxext-dev libgtk2.0-dev libgtk-3-dev libjpeg-dev libpng-dev libtiff-dev libxext-dev libxrender-dev python3-tk
RUN apt-get install -y x11-apps xauth

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm -f requirements.txt

#COPY root.bashrc /tmp
#RUN cat /tmp/root.bashrc >>/root/.bashrc && rm -f /tmp/root.bashrc
