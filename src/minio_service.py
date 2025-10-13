from env_settings import settings


async def upload_file(minio_client, file_content: bytes, file_name: str, content_type: str):
    async with minio_client as s3_client:
        upload_params = {
            'Bucket': settings.minio.bucket,
            'Key': file_name,
            'Body': file_content,
            'ContentType': content_type,
            'ContentDisposition': 'inline',
        }
        await s3_client.put_object(**upload_params)
