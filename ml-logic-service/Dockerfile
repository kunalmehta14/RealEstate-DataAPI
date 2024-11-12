FROM nvcr.io/nvidia/tensorflow:21.07-tf2-py3
ENV LANG en_US.utf8
#Update Ubuntu
RUN apt update && apt full-upgrade -y
RUN apt install \
    sudo -y \
    supervisor -y \
    cron \
    nano -y \
    pkg-config \
    libffi-dev \
    llvm-dev \
    llvm
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
# Install python and the python dependencies
RUN apt install python3-pip -y
# Create App Directory
RUN mkdir /opt/src
COPY ./src/requirements.txt /opt/src/requirements.txt
WORKDIR /opt/src
# RUN pip install -r requirements.txt
#Copy supervisoryd.conf configuration that defines the startup services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Add the cron job
# RUN crontab -l | { cat; echo "*/30 * * * * python3 /opt/src/plcscraper/main.py"; } | crontab -
EXPOSE 8008
#start startup services when the server starts
CMD ["/usr/bin/supervisord"]