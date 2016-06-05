# -*- coding: utf-8 -*-
# Copyright 2015 Vince Veselosky and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, print_function
from jinja2 import BaseLoader, TemplateNotFound
from botocore.exceptions import ClientError
import boto3
from gzip import GzipFile
from io import BytesIO
import posixpath as path


def gzip(content, filename=None, compresslevel=9):
    gzbuffer = BytesIO()
    gz = GzipFile(filename, 'wb', compresslevel, gzbuffer)
    gz.write(content)
    gz.close()
    return gzbuffer.getvalue()


def gunzip(gzcontent):
    gzbuffer = BytesIO(gzcontent)
    return GzipFile(None, 'rb', fileobj=gzbuffer).read()


class S3loader(BaseLoader):

    def __init__(self, bucket, prefix='', s3=None):
        self.bucket = bucket
        self.prefix = prefix
        self.s3 = s3 or boto3.client('s3')
        super(S3loader, self).__init__()

    def get_source(self, environment, template):
        if self.prefix:
            template = path.join(self.prefix, template)
        try:
            resp = self.s3.get_object(Bucket=self.bucket, Key=template)
        except ClientError as e:
            if "NoSuchKey" in e.__str__():
                raise TemplateNotFound(template)
            else:
                raise e
        if 'ContentEncoding' in resp and 'gzip' in resp['ContentEncoding']:
            body = gunzip(resp['Body'].read())
        else:
            body = resp['Body'].read()
        return (body.decode('utf-8'), None, lambda: True)

