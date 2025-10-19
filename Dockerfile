FROM python:3.12.10
ENV PYTHONUNBUFFERED True 
EXPOSE 5000
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]