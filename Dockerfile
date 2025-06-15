# Use an official Python runtime as a parent image
FROM python:3.9-slim
ENV PYHTONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /bot

# Copy the current directory contents into the container at /bot
COPY . /bot

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=World

# Run bot.py when the container launches
CMD ["python", "Main.py"]