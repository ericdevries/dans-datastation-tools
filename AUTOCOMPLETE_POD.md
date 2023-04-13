Autocomplete 
============

A PoC for moving all the commands to a single command, and put autocomplete on it. 

Instead of having these commands:
* dv-banner 
* dv-open-access-archeodepot
* dv-dataset-oai-harvest 

We would have a single command, with autocomplete:
* dv banner
* dv dataset oai-harvest

Note that this command name is just an example, it can be anything.

This uses the argparse subcommand functionality, like so

```python
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

# add autocomplete support
argcomplete.autocomplete(parser)
args = parser.parse_args()
```

The magic part is the autocomplete script, which has to be enabled like so:

```bash
eval "$(register-python-argcomplete dv)"
```

Now it will autocomplete for the `dv` command, which should map to the script above according to the pyproject.toml file.

## Requirements

For this to work on a machine, there are 2 requirements:
1. the default python install has `argcomplete` installed
2. the `register-python-argcomplete` script is added to `~/.bashrc` or `~/.zshrc` or `.profile` or whatever is applicable



