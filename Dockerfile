FROM python:3-alpine

WORKDIR /usr/src/mmcc
ENV PYTHONPATH /usr/src/mmcc

COPY ./backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./framework/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend/websocket_server.py .
COPY ./backend/functions.py .
COPY ./framework/mmcc_framework ./mmcc_framework

CMD [ "python", "./websocket_server.py"]

EXPOSE 8765