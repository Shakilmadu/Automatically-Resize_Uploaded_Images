
import boto3
from PIL import Image
import io

s3 = boto3.client('s3')


def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    # Download the image
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    image = Image.open(response['Body'])

    # Resize the image
    resized_image = image.resize((128, 128))
    output = io.BytesIO()
    resized_image.save(output, format=image.format)
    output.seek(0)

    # Upload the resized image
    s3.put_object(
        Bucket=bucket_name,
        Key=f"resized/{object_key}",
        Body=output
    )

    return {
        'statusCode': 200,
        'body': f"Resized image saved as resized/{object_key}"
    }

