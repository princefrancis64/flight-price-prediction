FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set Airflow environment variables
ENV AIRFLOW__CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE_ENABLE_XCOM_PICKLING=True

# Initialize Airflow database
RUN airflow db init

# Create Airflow admin user
RUN airflow users create -e prince.francis64@gmail.com -f Prince -l Francis -p admin -r Admin -u admin

# Change permissions for start.sh
RUN chmod 777 start.sh

# Install AWS CLI
RUN apt update -y && apt install awscli -y

# Set the entrypoint and default command
ENTRYPOINT ["/bin/sh"]
CMD ["start.sh"]
