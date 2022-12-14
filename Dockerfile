FROM python:3

ARG APP_PATH='/usr/src/app'

WORKDIR $APP_PATH

COPY requirements.txt .

RUN pip install -r requirements.txt

# Add user 
RUN groupadd -g 1000 app_user
RUN useradd -u 1000 -ms /bin/bash -g app_user app_user

# Copy existing application directory permissions
COPY --chown=app_user:app_user . $APP_PATH

RUN chown app_user:app_user -R $APP_PATH
RUN chmod 777 -R $APP_PATH
RUN chmod g+s -R  $APP_PATH

# Change current user to app_user
USER app_user

ENV FLASK_RUN_PORT=8000
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]