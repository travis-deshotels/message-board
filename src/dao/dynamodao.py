import datetime

import boto3
import uuid

from dto.message import DynamoMessage
from boto3.dynamodb.conditions import Key

db_resource = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')
table = db_resource.Table('message')
dynamo_message = DynamoMessage()


def get_all_messages():
    response = table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    # TODO fix sorting return data.sort(key=sort_func)
    return dynamo_message.get_messages(data)


def get_messages(days_of_messages, get_all=False):
    if get_all:
        return get_all_messages()
    else:
        response = table.query(
            KeyConditionExpression=Key('messageDate').eq(str(datetime.date.today() - datetime.timedelta(1)))
        )
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        return dynamo_message.get_messages(data)


def get_message(message_id):
    response = table.query(
        KeyConditionExpression=Key('messageUID').eq(message_id),
        IndexName='messageUID-index'
    )

    return dynamo_message.get_message(response['Items'][0]) if response['Items'] else None


def post_message(message, poster):
    table.put_item(
        Item={
            'messageUID': str(uuid.uuid4())[:8],
            'messageDate': str(datetime.date.today()),
            'messageTime': str(datetime.datetime.now().time()),
            'message': message,
            'poster': poster
        }
    )


def setup():
    db = boto3.client('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')
    db.create_table(
        TableName='message',
        KeySchema=[
            {
                'AttributeName': 'messageDate',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'messageTime',
                'KeyType': 'RANGE'
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'messageUID-index',
                'KeySchema': [
                    {
                        'AttributeName': 'messageUID',
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
                'AttributeName': 'messageDate',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'messageTime',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'messageUID',
                'AttributeType': 'S'
            }
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
