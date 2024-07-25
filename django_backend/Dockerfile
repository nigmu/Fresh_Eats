FROM python:3.9.13

WORKDIR /docker_cont_fresh_eats_prod

LABEL org.opencontainers.image.authors="nigmucode@gmail.com"

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader wordnet

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

