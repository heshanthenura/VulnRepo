FROM python:3.11-slim

WORKDIR /pawnshop

COPY static /pawnshop/static
COPY templates /pawnshop/templates
COPY database.db /pawnshop/database.db
COPY app.py /pawnshop/app.py
COPY requirements.txt /pawnshop/requirements.txt

RUN pip3 install -r /pawnshop/requirements.txt

EXPOSE 5000
CMD ["python3", "app.py"]