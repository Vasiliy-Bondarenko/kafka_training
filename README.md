Watch https://www.youtube.com/watch?v=06iRM1Ghr1k  
And this https://www.youtube.com/watch?v=JalUUBKdcA0


> Docker memory is allocated minimally at 8 GB. When using Docker Desktop for Mac, the default Docker memory allocation is 2 GB. You can change the default allocation to 8 GB in Docker > Preferences > Advanced.

- run `docker-compose up -d`  
- `docker-compose ps` - make sure all services are running  
- if not - restart with `docker-compose stop && docker-compose up -d`
- control with `docker-compose logs --tail=100 -f control-center`
- open in the browser [control center](http://localhost:9021/clusters) - it may take some time to start
- wait for 1 healthy cluster to appear

Congrats! You have a running Kafka cluster. 

- run `docker-compose exec app bash`
- to produce a few messages run  
`./start.sh`

name: PGS

Tasks: 1

Key converter class: 
org.apache.kafka.connect.storage.StringConverter

Topics:
users

Value converter class:
org.apache.kafka.connect.json.JsonConverter

## Connection
JDBC URL: 
jdbc:postgresql://db:8032/postgres

JDBC User:
postgres

JDBC Passowrd:
open

Dataabse Dialect:
PostgreSqlDatabaseDialect

Insert mode:
upsert

Primary Key Mode:
record_key

Auto-Create: true
Auto-Evolve: true
