# -*- coding:utf-8 -*-

"""
Gets remote ip
"""

def get_remote_addr(request):
    if 'REMOTE_ADDR' in request.META and request.META['REMOTE_ADDR']:
        return request.META['REMOTE_ADDR']
    return request.META.get('HTTP_X_FORWARDED_FOR', '127.0.0.1').split(', ')[0]
