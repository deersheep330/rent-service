FROM deersheep330/python-chrome-crontab

ENV TZ=Asia/Taipei

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

WORKDIR /home/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./rent ./rent
COPY ./main.py .
COPY ./cron_entrypoint.sh .
# COPY ./variables.ini .

# Run the command on container startup
CMD /usr/local/bin/python /home/app/main.py && /bin/bash ./cron_entrypoint.sh && tail -f /var/log/cron.log
# CMD ["cron", "-f"]

#Quick note about a gotcha:
#If you're adding a script file and telling cron to run it, remember to
#RUN chmod 0744 /the_script
#Cron fails silently if you forget.