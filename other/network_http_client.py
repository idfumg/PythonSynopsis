#!/usr/bin/env python

import http.client
import sys

def main():
    assert len(sys.argv) == 2, "Please enter {0} argument".format(sys.argv[0])

    conn = http.client.HTTPConnection(sys.argv[1])
    conn.request("GET", "/")
    response = conn.getresponse()
    print(response.status, response.reason)
    print(response.read())
    conn.close()

if __name__ == "__main__":
    main()
