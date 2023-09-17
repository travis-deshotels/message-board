# Message Board

## DynamoDB local
For offline DynamoDB run `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb` after downloading the DynamoDB Local jar.

## Docker and SQLite

* Create .msgconfig and populate it
* `docker build -t msgimg`
* `docker run -i --name msgboard -v <local path>/messageboard.db:/usr/app/data/messageboard.db msgimg`
* `docker start -i msgboard`
