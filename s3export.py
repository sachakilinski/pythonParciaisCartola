import boto3

s3 = boto3.resource('s3')
with open('parciais.html', 'r') as f:
    body = f.read()
print body
s3.Object('ilegrao', 'index.html').put(Body=body, ContentType='text/html', ACL='public-read')
