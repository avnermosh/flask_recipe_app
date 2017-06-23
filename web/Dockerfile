FROM python:3.6.1
MAINTAINER Patrick Kennedy <patkennedy79@gmail.com>

# Create the working directory
RUN mkdir -p /usr/src/app/web
WORKDIR /usr/src/app/web

# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)
COPY requirements.txt /usr/src/app/web
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /usr/src/app/web

