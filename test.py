import boto3
import boto.s3.connection

ACCESS_KEY_ID = 'AKIAIRKYLG7FE27K5HNQ'
SECRET_ACCESS_KEY = '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'
BUCKET = 'brian-website'

s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY
)

url = s3.generate_presigned_url('get_object',
                                Params={'Bucket': BUCKET, 'Key': 'static/downloads/resume.pdf'},
                                ExpiresIn=100)
print(url)