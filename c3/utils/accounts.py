# Copyright 2015 CityGrid Media, LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
'''
Utilities to deal with CGM-standard accounts
'''

import os
import sys


def get_account_name(account_id=None, mapfile=None):
    '''
    Returns the canonical name of the account passed in, or defaults to the
    account in the environment variable 'AWS_ACCOUNT_ID'
    >>> get_account_name(535530826599)
    'opsqa'
    '''
    if account_id is None:
        account_id = os.getenv('AWS_ACCOUNT_ID')
    if not account_id:
        return False
    return translate_account(account_id=account_id, mapfile=mapfile)

def get_account_id(account_name=None, mapfile=None):
    ''' Returns the AWS account ID. '''
    if account_name is None:
        return os.getenv('AWS_ACCOUNT_ID')
    else:
        return translate_account(account_name=account_name, mapfile=mapfile)


def translate_account(account_id=None, account_name=None, mapfile=None):
    ''' Translate account id to account name and back again. '''
    if not mapfile:
        mapfile = '%s/%s' % (
            os.getenv('AWS_CONF_DIR'), 'account_aliases_map.txt')
    try:
        mfile = open(mapfile, 'r')
    except IOError, msg:
        print >> sys.stderr, 'ERROR: %s' % msg
        return False
    for line in mfile.readlines():
        if len(line.split(':')) == 3:
            (aws_name, aws_id) = line.split(":")[-2:3]
            if account_id:
                if aws_id.rstrip() == account_id:
                    return aws_name
            elif account_name:
                if aws_name.rstrip() == account_name:
                    return aws_id
    if account_id:
        msg = "ERROR: Couldn't translate ID %s" % account_id
    elif account_name:
        msg = "ERROR: Couldn't translate ID %s" % account_id
    print >> sys.stderr, msg
    return None