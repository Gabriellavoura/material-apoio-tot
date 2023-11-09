import json

from utils.s3_instance import *
from botocore.client   import ClientError

# Função para fazer upload de um objeto em algum bucket.
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = instanciar_s3()
    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# instanciar_s3() - Função para instanciar um client do s3. 
# upload_file(file_name, bucket, object_name=None) - Função para fazer upload de um arquivo em um bucket do s3.
# Esta função já possui o s3_client instanciado dentro dele.