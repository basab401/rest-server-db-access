#!/usr/bin/env python3

# flake8: noqa
# noqa: E302,E501

import os
import boto3


class S3Access(object):
    ''' Class to abstract away s3 access via boto3 '''
    def __init__(self, bucket_name):
        self.s3_resource = boto3.resource('s3')
        self.bucket_obj = self.s3_resource.Bucket(name=bucket_name)

    def upload_file(self, file_path, object_name=None):
        ''' upload a file to an s3 bucket '''
        print('ENTER upload_file')
        if not object_name:
            object_name = os.path.basename(file_path)
        print('file_path:{} object_name:{}'.format(file_path, object_name))
        response = self.bucket_obj.upload_file(
                Filename=file_path, Key=object_name)
        return response

    def download_file(self, file_name, download_folder):
        ''' download a given file from an s3 bucket '''
        output = f'{download_folder}/{file_name}'
        self.bucket_obj.download_file(file_name, output)
        return output

    def list_files(self):
        ''' list files in a given s3 bucket '''
        contents = []
        for f in self.bucket_obj.objects.all():
            contents.append(f)
        return contents

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        pass