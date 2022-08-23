# README

This repository demonstrates a Publish/Subscribe mechanism to notify Service Workers on updates. The Service Workers can then do follow up SCIM requests to retrieve further details on the notified subjects.

As for the demonstration there are 2 Service Workers (SERVICE1 and SERVICE2) and 1 publisher process.
The Publisher randomly notifies a service worker and informs on the topics 'user' or 'group'.

Next step is to integrate with a SCIM server to do the follow up processing.

## Run the demo

You can run this demo by:

```
docker-compose build
docker-compose up -d
```

Then observe the processing by:

```
docker-compose logs -f
```
