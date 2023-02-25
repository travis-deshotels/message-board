import boto3
import uuid
import time


db_resource = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')
table = db_resource.Table('message')


def get_messages(number_of_messages, get_all=False):
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data


def get_message(message_id):
    response = table.get_item(Key={
        'messageuid': message_id
    })
    return response['Item']


def post_message(message, poster):
    response = table.put_item(
        Item={
            'messageuid': str(uuid.uuid4())[:8],
            'postedat': int(time.time()),
            'message': message,
            'poster': poster
        }
    )
    print(response)


def setup():
    db = boto3.client('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')
    db.create_table(
        TableName='message',
        KeySchema=[
            {
                'AttributeName': 'messageuid',
                'KeyType': 'HASH'
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'postedat-index',
                'KeySchema': [
                    {
                        'AttributeName': 'postedat',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'messageuid',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'postedat',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


if __name__ == '__main__':
    #setup()
    print(list(db_resource.tables.all()))
    #post_message('Hello from Dynamo!!', 'tnd')
