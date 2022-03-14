FROM python:3.9-slim

WORKDIR /mainSilverParakeet

COPY ./app ./app
COPY ./requirements ./requirements
COPY ./settings.py ./settings.py

RUN python3 -m venv venv
RUN . venv/bin/activate && pip3 install --upgrade pip && pip3 install --no-cache-dir --upgrade -r requirements/requirements.txt

EXPOSE 8000
ENV PATH /venv/bin:$PATH

CMD ["venv/bin/python3", "-m" ,"uvicorn", "--factory", "app:create_app", "--host", "0.0.0.0", "--port", "8000", "--interface", "wsgi"]
