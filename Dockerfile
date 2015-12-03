############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Ivan Ermilov

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip


# Get pip to download and install requirements:
RUN apt-get install -y python-openssl
RUN pip install numpy
RUN	pip install requests
RUN	pip install requests[security]
RUN	pip install SPARQLWrapper
RUN	pip install flask
RUN	pip install flask-wtf
RUN	pip install oauth2client pyopenssl ndg-httpsclient pyasn1
RUN	pip install gspread
RUN	pip install pymongo

# Copy the application folder inside the container
ADD / /taipan
ADD /server /taipan/server

ENV PYTHONPATH "${PYTHONPATH}:/taipan"

# Expose ports
EXPOSE 5000

# Set the default directory where CMD will execute
WORKDIR /taipan/server

# Set the default command to execute
# when creating a new container
# i.e. using CherryPy to serve the application
CMD python run.py
