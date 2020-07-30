#!/usr/bin/python
# -*- coding: utf-8 -*-
import re


def check_ipv4_valid(ip, allow_lo=True):
    if not ip:
        return False
    if not isinstance(ip, str):
        return False
    if ip in ['0.0.0.0', '255.255.255.255']:
        return False
    if not allow_lo and ip == '127.0.0.1':
        return False
    if len(ip) > 6 and ip[:6] == '224':
        return False
    if len(ip) > 10 and ip[:7] == '169.254':
        return False
    pattern = '^((2(5[0-5]|[0-4]\d)|[0-1]?\d{1,2})\.){3}(2(5[0-5]|[0-4]\d)|[0-1]?\d{1,2})$'
    if re.match(pattern, ip):
        return True
    return False
