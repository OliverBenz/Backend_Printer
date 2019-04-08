FROM python:3.6.3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 3004 available to the world outside this container
EXPOSE 3004

# Run app.py when the container launches
CMD ["python", "./rest_server.py"]