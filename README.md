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

### Runtime details...

You can take a in-depth look into the runtime dynamics of the different containers, here are some examples.

#### Publisher

```
docker-compose logs -f publisher
```

Will show something like:

```
publisher  | Starting publisher...
publisher  | 2022-08-24 08:18:58,652 INFO Enabling service: 'SERVICE1'...
publisher  | 2022-08-24 08:18:58,790 INFO Adding credentials for service: 'SERVICE1'...
publisher  | 2022-08-24 08:18:58,795 INFO Adding permissions for service: 'SERVICE1'...
publisher  | 2022-08-24 08:18:58,801 INFO Service: 'SERVICE1' is now enabled !
publisher  | 2022-08-24 08:18:58,801 INFO Enabling service: 'SERVICE2'...
publisher  | 2022-08-24 08:18:58,836 INFO Adding credentials for service: 'SERVICE2'...
publisher  | 2022-08-24 08:18:58,840 INFO Adding permissions for service: 'SERVICE2'...
publisher  | 2022-08-24 08:18:58,846 INFO Service: 'SERVICE2' is now enabled !
publisher  | 2022-08-24 08:18:58,846 INFO Notify SERVICE2 for update on 'group' value: '95134'...
publisher  | 2022-08-24 08:19:01,902 INFO Notify SERVICE1 for update on 'group' value: '24229'...
publisher  | 2022-08-24 08:19:04,909 INFO Notify SERVICE1 for update on 'group' value: '95161'...
publisher  | 2022-08-24 08:19:07,925 INFO Notify SERVICE2 for update on 'group' value: '22059'...
publisher  | 2022-08-24 08:19:10,939 INFO Notify SERVICE2 for update on 'group' value: '50472'...
```

#### Service 1

```
docker-compose logs -f service1
```

Will show something like:

```
service1 | Starting service: ...
service1 | 2022-08-24 08:19:03,575 INFO Connecting to amqp://SERVICE1:AA1@rabbit:5672/SERVICE1...
service1 | 2022-08-24 08:19:03,577 INFO Pika version 1.3.0 connecting to ('192.168.112.2', 5672)
....
service1 | 2022-08-24 08:19:03,582 INFO Created channel=1
service1 | 2022-08-24 08:19:03,588 INFO Start consuming...
service1 | 2022-08-24 08:19:04,918 INFO [GROUP:95161] Notification received !
service1 | 2022-08-24 08:19:16,982 INFO [USER:96903] Notification received !
service1 | 2022-08-24 08:19:22,998 INFO [USER:89902] Notification received !
service1 | 2022-08-24 08:19:29,044 INFO [GROUP:71659] Notification received !
service1 | 2022-08-24 08:19:32,050 INFO [GROUP:82134] Notification received !
service1 | 2022-08-24 08:19:35,068 INFO [USER:62532] Notification received !
```

### Management dashboard

And for the Rabit Manamegent dashboard you can go to http://localhost:15672 and inspect everything what is going on in the rabbit environment. Credentials can be found and adjusted off course in the **.env** file.

As a first excercise for the reader, add a service3 to the running environment...

Enjoy !
