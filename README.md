# Marmoset

Monkeying around with client specific PXE configurations.



## Requirements

* python 3.3+



## Setup

Create `marmoset.conf` before using marmoset! See `Configuration` for details.


## Configuration

The configuration file has to be placed in the app's root directory
as `marmoset.conf`. It is necessary to define a `PXELabel` section.
The first entry in this section will be the default label.

All other sections are optional and have defaults set.

An example file can be found as `marmoset.conf.example`.


## Usage

Marmoset can be used via CLI directly or as a HTTP server.


### CLI

To see all available subcommands and their aliases, just run the script
with the command:

    ./marmoset.py pxe


#### Create entries

Create an PXE entry with the default label:

    ./marmoset.py pxe create 3.4.5.6

Create an PXE entry for a non-default label:

    ./marmoset.py pxe create -l freebsd 3.4.5.6

If the used label has a callback method set that sets a custom root
password for the PXE boot target, you can provide a pasword: 

    ./marmoset.py pxe c -l freebsd -p SoSecretPW 3.4.5.6


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

List all currently set entries:

    curl -u admin:secret http://localhost:5000/pxe
    # {entries: [
    #   {"ip_address": "1.2.3.4", "label": "rescue"}
    # ]}
    
Create a new PXE config entry (label and password are optional)

    curl -u admin:secret --data 'ip_address=10.10.1.1&label=rescue&password=SeCrEt' \
    http://localhost:5000/pxe
    # 201 on success
    # 409 if there is already an entry

Check if there is an entry currently set

    curl -u admin:secret http://localhost:5000/pxe/10.10.1.1
    # 200 if found
    # 404 if not found

Destroy an entry

    curl -u admin:secret -X DELETE http://localhost:5000/pxe/10.10.1.1
    # 204 on success



## Issues

Find the code at [the git repo](https://www.aibor.de/cgit/marmoset/).

Contact code@aibor.de.

