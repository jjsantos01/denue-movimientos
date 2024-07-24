FROM python:3.6-slim
COPY requirements.txt deploy/requirements.txt
RUN pip install -r deploy/requirements.txt
COPY . deploy
EXPOSE 8501
WORKDIR deploy
CMD ["streamlit", "run", "app.py"]