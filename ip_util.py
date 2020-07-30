# -*- coding:utf-8 -*-

import re


class IPAddrException(Exception):
    def __init__(self, msg):
        self.__msg = msg

    def __repr__(self):
        return 'IPv4 address '


def check_ip_in_cidr(ip, cidr):
    """
    Check if IPv4 address in CIDR.
    :param ip: (str) IPv4 address
    :param cidr: (str) CIDR, ip/x and x must in [8, 16, 24, 32]
    :return: (bool) True if in
    """
    prefix, suf = cidr.split('/')
    suf = int(suf)
    if suf not in [8, 16, 24, 32]:
        raise IPAddrException('Invalid parameter cidr.')
    net = suf / 8
    cidr_prefix = '.'.join(prefix.split('.')[:net])
    ip_prefix = '.'.join(ip.split('.')[:net])
    if cidr_prefix != ip_prefix:
        return False
    return True


def check_ipv4_valid(ip, cidr=None, allow_lo=True):
    """
    Check if the IPv4 address is valid.
    :param ip: (str) IPv4 address
    :param cidr: (str or None) CIDR, ip/x and x must in [8, 16, 24, 32]
    :param allow_lo: (bool) if Loopback Address 127.0.0.1 is valid
    :return: (bool) True means ip is valid or False means not
    """
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
        if cidr:
            return check_ip_in_cidr(ip, cidr)
        return True
    return False


def check_ipv6_valid(ip, cidr=None, allow_lo=True):
    raise NotImplementedError()


def check_ip_valid(ip, **kwargs):
    version = kwargs.get('version', 4)
    cidr = kwargs.get('cidr', None)
    allow_lo = kwargs.get('allow_lo', True)
    if version == 4:
        return check_ipv4_valid(ip, cidr=cidr, allow_lo=allow_lo)
    elif version == 6:
        return check_ipv6_valid(ip, cidr=cidr, allow_lo=allow_lo)
    else:
        raise IPAddrException('Invalid parameter version.')


def ip2num(x):
    lst = []
    for i, j in enumerate(x.split('.')[::-1]):
        lst.append(256 ** i * int(j))
    return sum(lst)


def num2ip(x):
    lst = []
    for i in [3, 2, 1, 0]:
        cur = x / (256 ** i) % 256
        lst.append(str(cur))
    return '.'.join(lst)


def get_all_ips(start, end, excp=None):
    """
    Gets all IPv4 addresses for a range.
    :param start: (str) The first IPv4 address
    :param end: (str) The last one.
    :param excp: (list)
    :return: (list) all IPv4 addresses cover maybe invalid.
    """
    all_ips = []
    if not excp:
        for i in range(ip2num(start), ip2num(end) + 1):
            all_ips.append(num2ip(i))
    else:
        for i in range(ip2num(start), ip2num(end) + 1):
            cur_ip = num2ip(i)
            if cur_ip not in excp:
                all_ips.append(cur_ip)
    return all_ips
