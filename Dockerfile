# official python image
FROM python:3.10-alpine

# create directory for the app user
RUN mkdir -p /home/app && \
    addgroup -S app && adduser -S app -G app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/app
ENV API_VERIFY=True

# set workdir
WORKDIR $HOME

# install dependencies
RUN pip install flask requests gunicorn 'connexion[swagger-ui]'

# copy the API
COPY ./src/* $HOME/

# chown all the files to the app user
RUN chown -R app:app $HOME

# expose the port
EXPOSE 5000

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]