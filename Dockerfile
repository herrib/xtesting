FROM python:3

WORKDIR /usr/src/app

# Ajout du script Python dans /usr/src/app

COPY /home/herve/Containers/Xtesting/. ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python"]
CMD ["./test_url.py"]







