FROM python:3.12
COPY . .
RUN pip3 install -r requirements.txt
CMD python bot.py