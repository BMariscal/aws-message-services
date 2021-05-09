# aws-message-services (also emojis app)
  - simple app with bloated infrastructure for funsies
  
https://lumigo.io/blog/choosing-the-right-event-routing-on-aws-eventbridge-sns-or-sqs/

AWS EventBridge vs SQS
---
SQS is point to point: you send a message explicitly to an endpoint. 
Eventbridge is publish-subscribe: any number of clients can receive an 
event broadcast by a producer, without changing the producer.

AWS MQ
---
Amazon MQ is managed ActiveMQ. It has two main concepts: topics and queues. With a queue, you can have multiple consumers of a queue and each message will be delivered once; if there are no consumers when the message arrives, it sits in the queue until a consumer arrives. With a topic you can have multiple consumers and each message will be delivered once to each consumer, but if a consumer is offline when a message arrives they miss it.
https://github.com/aws-samples/amazon-mq-workshop

Python and MQ:
https://stackoverflow.com/questions/63720249/not-able-to-connect-to-amazonmq-via-mqtt-protocol-using-pythonpaho-mqtt-python

---
Tools:

- Django, Pillow, Gunicorn
- Postgres 
- Ngnix
- Docker
- Boto3: S3, SQS, EventBridge


----
![infrastructure](https://user-images.githubusercontent.com/13512876/117584078-916cc980-b0bf-11eb-9305-859ee9b7eb26.png)




TODO: 
- move db (currently a db container) to RDS
- Setup SNS + Lambda function to notify slack


----
- python3 -m venv env
- $ source env/bin/activate
- (env)$ pip install django==3.0.7
- (env)$ python manage.py migrate

Run in containers:
- make run

Rebuild images and run containers:

- make rebuild

Teardown:

- make teardown

