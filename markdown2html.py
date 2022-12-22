#!/usr/bin/python3
""" Script that transforme README.md en page HTML """

import re
import hashlib
import sys
import os

if __name__ == "__main__"
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("Missing " + sys.argv[1] + "\n")
        exit(1)

    with open(sys.argv[1]) as markdown_file:
        with open(sys.argv[2], 'w') as html_file:
            change_status = False
            ordered_status = False
            paragraph = False
            for line in markdown_file:
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                md5_tags = re.findall(r'\[\[.+?\]\]', line)
                md5_texts = re.findall(r'\[\[(.+?)\]\]', line)
                if md5_tags:
                    line = line.replace(md5_tags[0], hashlib.md5(
                        md5_texts[0].encode()).hexdigest())

                delete_c_tags = re.findall(r'\(\(.+?\)\)', line)
                delete_c_texts = re.findall(r'\(\((.+?)\)\)', line)
                if delete_c_tags:
                    delete_c_texts = ''.join(
                        c for c in delete_c_texts[0] if c not in 'Cc')
                    line = line.replace(delete_c_tags[0], delete_c_texts)

                length = len(line)
                headings = line.lstrip('#')
                heading_count = length - len(headings)
                unordered = line.lstrip('-')
                unordered_count = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_count = length - len(ordered)

                if 1 <= heading_count <= 6:
                    line = '<h{}>'.format(
                        heading_count) + headings.strip() + '</h{}>\n'.format(
                        heading_count)
                
                # * line = f'<h{heading_count}>{headings.strip()}</h{heading_count}>\n'

                if unordered_count:
                    if not change_status:
                        html_file.write('<ul>\n')
                        change_status = True
                    line = '<li>' + unordered.strip() + '</li>\n'
                if change_status and not unordered_count:
                    html_file.write('</ul>\n')
                    change_status = False

                if ordered_count:
                    if not ordered_status:
                        html_file.write('<ol>\n')
                        ordered_status = True
                    line = '<li>' + ordered.strip() + '</li>\n'
                if ordered_status and not ordered_count:
                    html_file.write('</ol>\n')
                    ordered_status = False

                if not (heading_count or change_status or ordered_status):
                    if not paragraph and length > 1:
                        html_file.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        html_file.write('<br/>\n')
                    elif paragraph:
                        html_file.write('</p>\n')
                        paragraph = False

                if length > 1:
                    html_file.write(line)

            if ordered_status:
                html_file.write('</ol>\n')
            if paragraph:
                html_file.write('</p>\n')

    exit(0)