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

Please not that the containers startup simultaneously but that they depend on the readiness of the rabbit container. As long as the rabbit container is not ready, the other container will fail to start properly. No worries though, they will constantly restart and at some moment the startup errors will go silent and interactions between the containers will word as designed. So, be patient !

Then observe the processing by:

```
docker-compose logs -f
```

And for the Rabit Manamegent dashboard you can go to http://localhost:15672 and inspect everything what is going on in the rabbit environment. Credentials can be found and adjusted off course in the **.env** file.

As a first excercise for the reader, add a service3 to the running environment...

Enjoy !
