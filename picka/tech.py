from struct import pack
from socket import inet_ntoa
from random import randint

from attrdict import AttrDict

import picka_utils

engine = picka_utils.engine_connection()


def mime_type():
    """Generates a random mime type.

    Returns:
      name (str): The full name of the mime type.
      extension (str): The file extension of the mime type.

    Examples:
      >>> mime_type()
      AttrDict({u'name': u'application.x-excel', u'extension': u'.xlv'})
    """
    res = engine.execute("SELECT name, extension FROM mimes ORDER BY  \
                         random() LIMIT 1;")
    return AttrDict([dict(d) for d in res.fetchall()][0])


def ipv4():
    return inet_ntoa(pack('>I', randint(1, 0xffffffff)))


def ipv6():
    # Prefix/L: fd
    # Global ID: 641f04c2ce
    # Subnet ID: b81a
    # Combine/CID: fd64:1f04:c2ce:b81a::/64
    # IPv6 addresses: fd64:1f04:c2ce:b81a::/64:XXXX:XXXX:XXXX:XXXXStart
    # Range: fd64:1f04:c2ce:b81a:0:0:0:0
    # End Range: fd64:1f04:c2ce:b81a:ffff:ffff:ffff:ffff
    # No. of hosts: 18446744073709551616
    pass
