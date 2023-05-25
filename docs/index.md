dans-datastation-tools
======================

Command line utilities for Data Station application management

SYNOPSIS
--------

```bash
pip3 install dans-datastation-tools

# To find out what a command does, use <command> --help, e.g.:
# dans-bag-validate --help

# Below is a partial list of commands. Commands are grouped by the application they target. 
# Commands in a group have the same prefix so you can use command line completion to find 
# all commands in a group. For example, to find all commands targeting Dataverse, 
# type `dv-` and press the tab key twice. This will list all commands starting with `dv-`.
# Some commands have subcommands, you can find the subcommands with the --help option.

# DANS bag validation
dans-bag-validate

# Commands targeting Dataverse start with dv-, e.g.:

# Dataverse banner management
dv-banner 

# Commands targeting Dataverse datasets start with dv-dataset-, e.g.:
dv-dataset-delete-draft 
dv-dataset-destroy
dv-dataset-destroy-migration-placeholder  
dv-dataset-find-by-role-assignment

# Dataverse user management
dv-user-import

# Ingest flow management
ingest-flow
```

DESCRIPTION
-----------

This module contains a variety of commands to facilitate DANS Data Station management. To find out what a command does,
use `<command> --help`. See the comments in the SYNOPSIS section above to get an idea of what commands are available.

### Batch processing of datasets

Some of the commands targeting Dataverse datasets can be used to process a large number of datasets in a batch. These
commands take a trailing argument `pid_or_pids_file`. As the name suggests, this argument can be either a single PID or
a file containing a list of PIDs. The file should contain one PID per line. These commands usually have the following
options:

* `--wait-between-items`: the number of seconds to wait between processing each dataset. This is useful to avoid
  overloading the server.
* `--fail-fast`: fail on the first error. If this option is not given, the command will continue processing the
  remaining datasets after an error has occurred.
* `--report-file`: the name of a CSV file in which a summary of the results will be written. The file will be created
  if it does not exist, otherwise it will be overwritten.

EXAMPLES
--------

### Processing JSON output of `dans-bag-validate` with jq

The JSON output of this command can be queried with `jq`. This tool has a very good
[manual](https://stedolan.github.io/jq/manual/){:target=_blank}. However, to get you started, here are some example
queries:

```bash
dans-bag-validate <target> > ~/results.json

# Print only the bag location and the violations
cat results.json 

# Count the number of bags that are non-compliant
cat results.json | jq '[.[] | select(."Is compliant" == false)] | length'

# Get the paths to the *deposits* containing valid bags. Note that "Bag location" is one level too deep, that's why we need to remove the 
# last path element. The detour through to_entries seems necessary to get rid of the array structure around the results.
cat results.json | select(."Is compliant" == true)] | map(."Bag location") | map(split("/") | .[:-1] | join("/")) | to_entries[] | "\(.value)"
```

INSTALLATION & CONFIGURATION
----------------------------

### Installation

#### For the current user 
This is the recommended way, when installing on your own machine.
  
```bash
pip3 install --user dans-datastation-tools
```
  
 You may have to add the directory where `pip3` installs the command to the `PATH` manually.

#### Globally 
This is useful when installing on a server where the commands need to be shared by multiple users.

```bash
sudo pip3 install dans-datastation-tools
```

### Configuration

The configuration file is called `.dans-datastation-tools.yml`. Each command starts by looking for this file in the
current working directory and then in the user's home directory. If it is not found in either location it is
instantiated with some default and placeholder values in the current directory. It is recommended that you move this
file to your home directory. Using the configuration file from the current working directory is mainly useful for
development.

For the available configuration options and their meaning, see the explanatory comments in the configuration file
itself.

