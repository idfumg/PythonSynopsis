#!/usr/bin/env python3

import http.client
import ssl
import sys

def main():
    assert len(sys.argv) == 2, "Please enter {0} argument".format(sys.argv[0])

    context = ssl.create_default_context()
    conn = http.client.HTTPSConnection(sys.argv[1], 443, context=context)

    conn.request("GET", "/")
    resp = conn.getresponse()

    print(resp.status, resp.reason)
    print(resp.read())

    conn.close()

if __name__ == "__main__":
    main()
