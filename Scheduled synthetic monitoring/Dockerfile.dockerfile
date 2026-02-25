FROM python:3.10
WORKDIR /app
COPY monitor.py .
RUN pip install requests
CMD ["python", "monitor.py"]