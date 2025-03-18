FROM python:3.8

# Dependencies:
#   Python version **<3.9**.
#   Git version **>=2.38.0**.

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the SpaCy language model
RUN python -m spacy download en_core_web_sm

# Install Git
RUN apt-get update && apt-get install -y git

# Create the Testing directory as a concrete path
RUN mkdir -p /app/Testing

# Copy the entire project directory into the container
COPY . .

# Uncomment the command below to execute your script automatically
CMD ["python", "harness.py"]
