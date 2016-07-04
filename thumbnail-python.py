__author__ = 'Andrew jackson'


import json
import urllib
import boto3
import cStringIO
from PIL import Image

print('Loading function')

s3 = boto3.client('s3')
sizes = [(120,120), (720,720), (1600,1600)]

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')

    if key.find("thumbnail") == -1:
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            print("CONTENT TYPE: " + response['ContentType'])

            if response['ContentType'] == "image/jpeg":
                buffer = cStringIO.StringIO(response['Body'].read())
                #buffer = response['Body'].read()
                for size in sizes:
                    destKey = "thumbnail_%s_%s" % (str(size[0]), key)
                    strThumb = cStringIO.StringIO()

                    try:
                        print "try open image"
                        img = Image.open(buffer)
                        print "try resize image"
                        img.thumbnail(size)
                        print "try save thumb to string"
                        img.save(strThumb, 'JPEG')

                    except Exception as e:
                        print(e)
                        print('Error opening or resizing img')

                    try:
                        print "try write stringIO to S3"
                        s3.put_object(Bucket=bucket, Key=destKey, ContentType=response['ContentType'], Body=strThumb.getvalue())
                        strThumb.close()
                        #s3.put_object(Bucket=bucket, Key=destKey, ContentType=response['ContentType'], Body=buffer)
                        print "created ", destKey

                    except Exception as e:
                        print(e)
                        print('Error writing file to S3')

            return response['ContentType']
        except Exception as e:
            print(e)
            print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
            raise e