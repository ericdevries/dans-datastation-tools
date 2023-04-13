#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argparse

from datastation.config import init
import argcomplete


def PidCompleter(**kwargs):
    print(kwargs)
    return ['doi:123', 'doi:543']

def main():
    parser = argparse.ArgumentParser(description='The global command')
    parser.add_argument("-v", help="Verbose", action="store_true")
    parser.add_argument("-vv", help="Very verbose", action="store_true")
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_user = subparsers.add_parser('import-user', help='import-user help')
    parser_user.add_argument("user", help="The user to import")
    parser_user.add_argument("-f", "--file", help="Newline separated file with users to import")

    parser_user = subparsers.add_parser('verify-dataset', help='verify-dataset help')
    parser_user.add_argument("pid", help="A dataset pid").completer = PidCompleter
    parser_user.add_argument("-f", "--file", help="Newline separated file with pids to verify")
    parser_user.add_argument("-o", "--output", help="Output file")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    print(args)


if __name__ == '__main__':
    main()