
import re

import boto3  # type: ignore
from botocore.client import Config  # type: ignore


def decompose_s3_url(url):

    pattern = r'^https:\/\/(?P<bucket>[\w.-]+)\.s3\.(?P<region>[\w-]+)\.amazonaws\.com\/(?P<key>.+)$'

    match = re.match(pattern, url)

    if match:
        bucket = match.group('bucket')
        region = match.group('region')
        key = match.group('key')
        return {
            'bucket': bucket,
            'region': region,
            'key': key
        }
    else:
        raise ValueError('No match found.')


seconds_in_day = 24 * 60 * 60


def get_presigned_url(url: str, expiration=seconds_in_day):
    components = decompose_s3_url(url)
    bucket = components['bucket']
    region = components['region']
    key = components['key']
    s3 = boto3.client('s3', config=Config(
        signature_version='s3v4'), region_name=region)
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )
    return url
