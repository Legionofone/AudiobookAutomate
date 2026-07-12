FROM python:3.12-alpine
# Or any preferred Python version.
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD main.py .
CMD ["python3", "-u", "./main.py"]
# Or enter the name of your unique directory and parameter set.
