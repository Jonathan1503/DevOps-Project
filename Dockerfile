FROM alpine:3.14

RUN apk add py3-pip \
    && pip install --upgrade pip

WORKDIR /app
COPY . /app/


RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python3", "application.py"]
##Confguración New Relic
RUN pip install newrelic
ENV NEW_RELIC_APP_NAME="entrega4"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
#INGEST_License
ENV NEW_RELIC_LICENSE_KEY=6D90875E0736835CFB89DA3C0AF60695D0B118BDDB331D0F25E9D0BD5EFE4110
ENV NEW_RELIC_LOG_LEVEL=info
# etc.

ENTRYPOINT ["newrelic-admin", "run-program"]

