# PUSH LIKE THIS docker push us-west1-docker.pkg.dev/opportune-geode-459012-k2/lamb/lamb:v0.1.0
# TO DELETE AN IMAGE gcloud artifacts docker tags delete LOCATION-docker.pkg.dev/PROJECT/REPOSITORY/IMAGE:TAG
# Run it like this: docker run --name lamb -p 5000:8000 -v ~/code/python/polyylop.io/scr/logs:/app/logs -v ~/code
#/python/polyylop.io/scr:/app/data lamb-0.1.0:latest
# This will make the logs and the database be exposed to the host server folders in scr
# Build it like this: docker build -t lamb-0.1.0 .
# Use the official Python 3.13 slim image as the base.
# This provides a minimal OS with Python installed, which is
# a great starting point for a lean and efficient image.
FROM python:3.13-slim

# Set the working directory for the application. This directory
# will contain all of our application's files inside the container.
WORKDIR /app

# The following block handles the installation of micromamba from scratch.
# We first update the package list and install necessary tools like 'curl'
# to download the micromamba binary, and 'tar' to extract it.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    bzip2 \
    tar && \
    # Download the micromamba binary to a temporary file.
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest > /tmp/micromamba.tar.bz2 && \
    # Extract the binary to /usr/local/bin, stripping the 'bin/' path component.
    tar -xvjf /tmp/micromamba.tar.bz2 --strip-components=1 -C /usr/local/bin bin/micromamba && \
    # Clean up the system packages and caches to minimize the final image size.
    apt-get purge -y --auto-remove curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/micromamba.tar.bz2

# Now, we create the micromamba environment and install 'uv' into it.
# We use the 'uv' package from the 'conda-forge' channel.
# We explicitly call the micromamba binary by its full path for reliability.
RUN /usr/local/bin/micromamba create -yn app-env python=3.13 && \
    /usr/local/bin/micromamba clean --all --yes

# Copy the requirements.txt file into the container. It's crucial to do this
# before installing the dependencies to leverage Docker's build cache.
COPY requirements.txt .

# Use 'micromamba run' to execute the 'uv pip install' command within the
# newly created 'app-env' environment. This correctly installs all dependencies
# listed in the requirements.txt file with 'uv's superior speed and efficiency.
# We again use the full path to the micromamba executable for reliability.
RUN /usr/local/bin/micromamba run -n app-env pip install uv
RUN /usr/local/bin/micromamba run -n app-env uv pip install -r requirements.txt

# Copy the rest of the application's source code. We do this as a separate
# step to take advantage of Docker's layer caching; if requirements don't change,
# this step will be faster on subsequent builds.
COPY . .

# Expose the port on which the application will run.
EXPOSE 5000

# Specify the command to run the application using Gunicorn from the new environment.
# The `micromamba run` command ensures the application is executed within the correct
# 'app-env' environment, which contains all the required packages.
# The `CMD` also uses the full path for maximum reliability.
CMD ["/usr/local/bin/micromamba", "run", "-n", "app-env", "gunicorn", "--bind", "0.0.0.0:8000", "app:flask_app"]
