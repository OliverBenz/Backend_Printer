FROM python:3.7

# Set the working directory to /app
WORKDIR /printerbackend

# Copy the current directory contents into the container at /app
COPY . /printerbackend

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 3004 available to the world outside this container
EXPOSE 3004

# Run app.py when the container launches
CMD ["python", "main.py"]