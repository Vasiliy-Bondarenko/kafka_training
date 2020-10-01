## Create a Kafka cluster
- `cp .env.example .env`
- Go to https://confluent.cloud/
- Register a new account if you don't have it yet
- Register an environment
- Create a cluster of Basic type in any of cloud environments (i was doing on AWS)
- Open Cluster Settings and take a "Bootstrap server" URL and put it into .env
- Go to API access > create a key > Next > copy-paste key and secret into .env 
- Don't forget to save credentials on the page
- Please be aware that API credentials can start working after a few minutes, not immediately, so if you see authentication error on the next steps - just wait for a few minutes.

## Login into Confluent Cloud
- log in to your Confluent Cloud cluster: `./ccloud.sh login --save`  
Your output should resemble:
```
Enter your Confluent credentials:
Email: jdoe@myemail.io
Password:

Logged in as jdoe@myemail.io
Using environment t118 ("default")
```
- Run this command to view your cluster.: `./ccloud.sh kafka cluster list`  
Your output should resemble:
```
      Id      |       Name        | Provider |   Region    | Durability | Status
+-------------+-------------------+----------+-------------+------------+--------+
    lkc-emmox | My first cluster  | gcp      | us-central1 | LOW        | UP
    lkc-low0y | My second cluster | gcp      | us-central1 | LOW        | UP
```
- Run this command to designate the active cluster.
`./ccloud.sh kafka cluster use CLUSTER_ID`  

- Initialize topics `./init_topics.sh`   
You should see something like `Created topic "logs".`

## Schema Registry
- Go to [https://confluent.cloud/](https://confluent.cloud/)
- Open your environment / Settings tab / Schema Registry API access [screenshot](http://joxi.ru/DmB4Dv7i4dVRjA)
- Copy-paste Schema Registry endpoint into .env
- Create new key and copy-paste credentials into .env
- Give it any description, click checkbox and click "Continue"

## Start the project
- run `docker-compose up -d`  
- `docker-compose ps` - make sure all services are running
- open in the browser [Connect UI](http://localhost:8007) - it may take some time to start. After "connect" service is started it will be at least one connector loaded (make sure you see "logs" connector running)
- control with `docker-compose logs -f connect` if needed

Congrats! You have a running Kafka environment. 


## More information
- [Faust overview](https://www.youtube.com/watch?v=Ik1PBbCWcTc)
- [AVRO specs](http://avro.apache.org/docs/current/spec.html)
