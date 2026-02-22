FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy clean requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source files
COPY . .

RUN pip install -e .

# Start an interactive shell by default
CMD ["bash"]
