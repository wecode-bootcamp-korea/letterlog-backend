import uuid, boto3, logging

from django.conf    import settings
from django.http    import JsonResponse

class AWSAPI:
    def __init__(self):
        self.bucket      = settings.AWS_S3_BUCKET
        self.storage_url = f'https://s3.ap-northeast-2.amazonaws.com/{self.bucket}/'
        self.client      = boto3.client(
            's3',
            aws_access_key_id     = settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_S3_ACCESS_KEY
        )

    def upload_file(self, file):
        try :
            filename = uuid.uuid4().hex
            self.client.upload_fileobj(
                file,
                self.bucket,
                filename,
                ExtraArgs = {
                    "ContentType": file.content_type,
                }
            )

        except Exception as e:
            logging.error(f"message : {e}")

            return JsonResponse({"message": "FAIL_TO_UPLOAD"}, status=422)

        return self.storage_url + filename
