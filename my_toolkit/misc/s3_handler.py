import os.path
from io import StringIO
import json

import boto3
import pandas as pd

s3 = boto3.client('s3')
bucket = 'bucket

# Layer 0
def read_as_str(key, folder):
    response = s3.get_object(Bucket=bucket, Key=f'{folder}/{key}')
    ret = response['Body'].read().decode('utf-8')
    print(f"Read file from S3/f'{folder}/{key}': {len(ret)=}.")
    return ret


def write_as_str(s, key, folder):
    s3.put_object(Body=s, Bucket=bucket, Key=f"{folder}/{key}")
    print(f"Object with {len(s)} is put on {folder}/{key} as JSON file.")


#Layer 1
def read_json(key, folder):
    file_str = read_as_str(key, folder)
    _dict = json.loads(file_str)
    return _dict


def write_json(_dict, key, folder):
    binary_str = json.dumps(_dict)  # .encode('ascii')
    write_as_str(binary_str, key, folder)


def read_df(key, folder):
    file_str = read_as_str(key, folder)
    csvStringIO = StringIO(file_str)
    df = pd.read_csv(csvStringIO, sep=",", header=None)
    return df


def write_df(df, key, folder):
    write_as_str(df.to_csv(), key, folder)
