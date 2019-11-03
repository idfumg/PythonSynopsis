#!/bin/env python

import optparse

def main():
    parser = optparse.OptionParser()
    parser.add_option("-w", "--maxwidth", dest = "maxwidth", type = "int",
                      help = ("the maximum number of characters that can be output "
                              "to string fields [default: %default]"))
    parser.add_option("-f", "--format", dest = "format",
                      help = ("the format used for outputting numbers"
                              " [default: %default]"))
    parser.set_defaults(maxwidth = 100, format = ".0f")
    opts, args = parser.parse_args()
    print(opts)
    print(args)

main()
