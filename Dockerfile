FROM python:3.5

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . .

CMD ["/bin/bash"]