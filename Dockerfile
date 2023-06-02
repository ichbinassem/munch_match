FROM python:3.6-alpine3.10
MAINTAINER Luis Fernando "luiscerqueira@uni.minerva.edu"

COPY requirements.txt .

# Install postgres libraries so that the pip install succeeds.
# We then immediately remove the unnecessary dependency.
RUN apk update && \
 apk add python3 postgresql-libs && \
 apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the environment variables for Flask
ENV FLASK_APP=app

# Run the flask command when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
