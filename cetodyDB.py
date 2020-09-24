import boto3

ceclient = boto3.client('ce')
#creating a dynamodb object for dynamodb service
dynamoDB = boto3.resource("dynamodb")
#creating a table object to get the table name from dynamodb

client = boto3.client("dynamodb")

def lambda_handler(event,context):
    alias = boto3.client('iam').list_account_aliases()['AccountAliases'][0]
    print (alias)
    cclient = boto3.client("sts", aws_access_key_id='AKIATKKJAOPD4GW2YZTV', aws_secret_access_key='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')
    account_id = cclient.get_caller_identity()["Account"]
    print(account_id)
    response = client.list_tables()
    if 'ram' not in response['TableNames']:
        #print(__file__)
        table = dynamoDB.create_table(
            TableName='ram',
            KeySchema=[
                {
                    'AttributeName': 'Year',
                    'KeyType': 'HASH'  
                },
                {
                    'AttributeName': 'Month',
                    'KeyType': 'RANGE'  
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Year',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Month',
                    'AttributeType': 'S'
                },
       
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 3,
                'WriteCapacityUnits': 3
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='ram')
    tableram = dynamoDB.Table("ram")

       
    response = ceclient.get_cost_and_usage(
    TimePeriod={
        'Start': '2020-08-01',
        'End': '2020-09-30'
    },
    Granularity='MONTHLY',
    Filter = {
    'Dimensions':
        {
        'Key' : 'INSTANCE_TYPE',
        'Values': ['t2.micro']
        }
    },
    Metrics=[
        'UsageQuantity',
    ]
     
    )
    
    for item in response['ResultsByTime']:
        year,month,date = item['TimePeriod']['Start'].split('-')
        unit = item['Total']['UsageQuantity']['Amount']
        tableram.put_item(
            Item = {
                "Unit": unit,
                "Year": int(year),
                "Month": int(month),
                "Account Name": alias,
                "Account Number": account_id
            }
        )



    
    
