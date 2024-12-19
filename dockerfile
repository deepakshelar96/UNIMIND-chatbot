#Use a lightweight Python image
FROM python:3.9-slim


# Set the working directory
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy the local code to the container
COPY . /app

# Copy the requirements file and install the required Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Install the MySQL client
RUN apt-get update && apt-get install -y default-mysql-client


# Expose the ports for Streamlit and LLAMA2 server (FastAPI)
EXPOSE 8501
EXPOSE 8000

# Copy supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Command to run supervisor, which will manage both processes
CMD ["/usr/bin/supervisord"]

