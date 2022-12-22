#!/usr/bin/python3

if __name__ == "__main__":
    import sys
    import os.path
    import re
    import hashlib

    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)
    
    if not os.path.isfile(sys.argv[1]):
        print("Missing {}".format(sys.argv[1]))
        sys.exit(1)

    with open(sys.argv[0]) as read:
        with open(sys.argv[1], 'w') as html:
            for line in read:
                length = len(line)
                headings = line.lstrip('#')
                heading_num = length - len(headings)

                if heading_num > 0:
                    line = '<h{}>'.format(heading_num) + headings.strip() + '</h{}>\n'.format(heading_num)

                if length > 1:
                    html.write(line)
    exit (0)
