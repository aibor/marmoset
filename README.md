# Marmoset

Monkeying around with client specific PXE configurations.



## Requirements

* python 3.3+



## Setup

Update `settings.py` before using marmoset!



## Usage

Marmoset can be used via CLI directly or as a HTTP server.


### CLI

To see all available subcommands and their aliases, just run the script
with the command:

    ./marmoset.py pxe


#### Create entries

Create an PXE entry with the default template:

    ./marmoset.py pxe create 3.4.5.6

Create an PXE entry for a non-default template:

    ./marmoset.py pxe create -t freebsd 3.4.5.6

If you need to do some additional magic after creating an entry, a
command can be passed, which is called after successfully creating the
entry. It will get passed the template name, the IP address and the
path to the entry file as arguments.

    ./marmoset.py pxe c -t freebsd -c /path/to/script 3.4.5.6


#### List entries

List all entries:

    ./marmoset.py pxe list


#### Remove entries

Remove the entry for an IP address:

    ./marmoset.py pxe remove 3.4.5.6


### HTTP server

Start it like this:

    ./marmoset.py server


#### Routes

Create a new PXE config entry

    curl -u admin:secret --data 'ip_address=10.10.1.1' http://localhost:5000/pxe
    # 201 on success
    # 409 if there is already an entry

Check if there is an entry currently

    curl -u admin:secret http://localhost:5000/pxe/10.10.1.1
    # 200 if found
    # 404 if not found

Destroy an entry

    curl -u admin:secret -X DELETE http://localhost:5000/pxe/10.10.1.1
    # 204 on success



## Issues

Find the code at [the git repo](https://www.aibor.de/cgit/marmoset/).

Contact code@aibor.de.

