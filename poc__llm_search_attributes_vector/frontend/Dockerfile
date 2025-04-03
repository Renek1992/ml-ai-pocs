
FROM python:3.12-slim

COPY requirements.txt frontend/requirements.txt
WORKDIR /frontend

RUN pip install -r requirements.txt
COPY . /frontend

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]

CMD ["Home.py"]