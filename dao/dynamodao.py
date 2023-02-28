import boto3
import uuid
import time

from boto3.dynamodb.conditions import Attr

db_resource = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')
table = db_resource.Table('message')
text_table = db_resource.Table('message_text')


def get_messages(days_of_messages, get_all=False):
    current_time = int(time.time())
    one_day = 86400

    if get_all:
        response = table.scan()
    else:
        response = table.scan(FilterExpression=Attr('postedat').lt(current_time) &
                                               Attr('postedat').gt(current_time - (int(days_of_messages) * one_day)))
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data


def get_message(message_id):
    response_text_table = text_table.get_item(Key={
        'messageuid': message_id
    })
    message_text = response_text_table['Item']['message']
    response = table.get_item(Key={
        'messageuid': message_id
    })
    response['Item']['message'] = message_text

    return response['Item']


def post_message(message, poster):
    message_uid = str(uuid.uuid4())[:8]
    table.put_item(
        Item={
            'messageuid': message_uid,
            'postedat': int(time.time()),
            'message': message[0:39],
            'poster': poster
        }
    )
    text_table.put_item(
        Item={
            'messageuid': message_uid,
            'message': message,
        }
    )


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

    db.create_table(
        TableName='message_text',
        KeySchema=[
            {
                'AttributeName': 'messageuid',
                'KeyType': 'HASH'
            }
        ],

        AttributeDefinitions=[
            {
                'AttributeName': 'messageuid',
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
