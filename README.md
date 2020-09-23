TODO:
- [ ] Use AVRO
- [ ] Connection to Schema Registry

## Create a Kafka cluster
- Go to https://confluent.cloud/
- Register a new account if you don't have it yet
- Register an environment
- Create a cluster of Basic type in any of cloud environments (i was doing on AWS)
- Open Cluster Settings and take a "Bootstrap server" URL and put it into .env
- Go to API access > create a key > Next > copy-paste key and secret into .env 
- Don't forget to save credentials on the page
- Please be aware that API credentials can start working after a few minutes, not immediately, so if you see authentication error on the next steps - just wait for a few minutes.

- Install the Confluent Cloud CLI
    `curl -L --http1.1 https://cnfl.io/ccloud-cli | sh -s -- -b /usr/local/bin`
- log in to your Confluent Cloud cluster: `ccloud login`  
Your output should resemble:
```
Enter your Confluent credentials:
Email: jdoe@myemail.io
Password:

Logged in as jdoe@myemail.io
Using environment t118 ("default")
```
- Run this command to view your cluster.: `ccloud kafka cluster list`  
Your output should resemble:
```
      Id      |       Name        | Provider |   Region    | Durability | Status
+-------------+-------------------+----------+-------------+------------+--------+
    lkc-emmox | My first cluster  | gcp      | us-central1 | LOW        | UP
    lkc-low0y | My second cluster | gcp      | us-central1 | LOW        | UP
```
- Run this command to designate the active cluster.
`ccloud kafka cluster use CLUSTER_ID`  

- Initialize topics `./init.sh`   
You should see something like `Created topic "users".`


- run `docker-compose up -d`  
- `docker-compose ps` - make sure all services are running
- it may take about 2 minutes to start and connect to Kafka in the cloud  
- control with `docker-compose logs -f connect`
- open in the browser [Connect UI](http://localhost:8007) - it may take some time to start

Congrats! You have a running Kafka environment. 

- run `docker-compose exec app bash`
- run `./init.sh` to create topics in you Kafka cluster
- run `pip install python-dotenv` just in case you are running old image :)
- to produce a few messages run `./start.sh`
- go to [Connect UI](http://localhost:8007)
- create new connector of type JDBC Sink
- switch to JSON tab
- copy-paste content from [this file](./connector_PGS_config.json)
- click "Create"
- now you can connect to your local database with any sql client (db: localhost, port: 8032, user: postgres, db: postgres, password: open)
- if everything is working you should see `users` table and new records being created or updated every second
- if do not see the table or no records:
    - make sure you run `./start.sh` in `app` container
    - go to https://confluent.cloud/ and make sure you have new messages being produced in `users` topic
    - check logs `docker-compose logs -f connect` if you have any problems connecting to kafka - you should see some errors 

Assignment:
- create new `accounts` table in the database
- create a few records
- using [Connect UI](http://localhost:8007) create 'Source JDBC' connector to pull data from database and push it into Kafka.
- make sure new records are created in Kafka
