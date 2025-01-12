FROM python:3.10

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install necessary system dependencies for Basemap and GDAL
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin &&\
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt ./

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt 

# Copy the rest of the application code into the container
COPY . .

# Expose the appropriate port for the app
EXPOSE 8000

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
