FROM ubuntu:latest
ENV LANG en_US.utf8
RUN apt update && apt full-upgrade -y
RUN apt install \
    sudo -y \
    supervisor -y \
    nano -y \
    pkg-config -y \
    libmysqlclient-dev
# Configure TimeZone
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt install python3-pip -y
# Create App Directory
RUN mkdir /opt/app
# RUN chown administrator:root /opt/app
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
#Copy supervisoryd.conf configuration that defines the startup services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
#Copy the logging script and make it executable
USER root
RUN ln -sf /proc/1/fd/1 /var/log/debug.log
EXPOSE 80
#start startup services when the server starts
CMD ["/usr/bin/supervisord"]