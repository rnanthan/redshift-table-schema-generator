from common.log_util import log
from datetime import datetime


def copy_to_bucket(s3_resource, source_bucket_name, target_bucket_name, object_key):
    """
    Copy object in one bucket to another bucket
    :param s3_resource: S3 Resource
    :param source_bucket_name: Source Bucket name
    :param target_bucket_name: Target Bucket Name
    :param object_key: Object to be copied
    :return:
    """
    copy_source = {
        'Bucket': source_bucket_name,
        'Key': object_key
    }
    s3_resource.Bucket(target_bucket_name).copy(copy_source, object_key)


def upload_csv_file_to_s3(client, file_name, s3_bucket, s3_prefix):
    """
    Update the CVS file to S3 bucket
    :param client: s3 client
    :param file_name: S3 prefix
    :param s3_bucket: File name
    :param s3_prefix: S3 bucket name to upload the CSV file
    """
    try:
        time_now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        client.meta.client.upload_file('/tmp/' + file_name + '.csv', s3_bucket, s3_prefix + '/' + file_name + '_' +
                                       time_now + '.csv')
    except Exception as ex:
        log.error(f'Error occurred while uploading the file to S3. {ex}')
        raise


def get_object(client, s3_bucket, object_key):
    """
    Getting object from S3.
    :param client: s3 client
    :param s3_bucket: S3 bucket name
    :param object_key: Object key
    :return: S3 object
    """
    response = client.get_object(Bucket=s3_bucket, Key=object_key)
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    if status == 200:
        return response.get("Body")
    else:
        log.error(f'Error occurred while getting object from S3. {status}')
        raise
