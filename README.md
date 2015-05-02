# Marmoset

Monkeying around with virtual machines and pxe configs.



## Setup

Create `marmoset.conf` before using marmoset! See `Configuration` for details.


### Requirements

* python 3.3+
* libvirt-python3 (or similar package that provides libvirt python
  bindings)
* flask


### Configuration

The configuration file has to be placed in the app's root directory
as `marmoset.conf`. It is necessary to define a `PXELabel` section.
The first entry in this section will be the default label.

All other sections are optional and have defaults set.
An example file can be found as `marmoset.conf.example`.

If you want to customize the XML templates for libvirt objects, copy
the template dir `marmoset/virt/templates/` and specify the new path
in the `Libvirt` section.


## Usage

Marmoset can be used via CLI directly or as a HTTP server.


### CLI

To see all available subcommands and their aliases, just run the script
with the command:

    $ ./marmoset.py -h

Each subcommand provides its own help text:

    $ ./marmoset.py pxe -h


#### PXE

##### Create entries

Create an PXE entry with the default label:

    $ ./marmoset.py pxe create 3.4.5.6

Create an PXE entry for a non-default label:

    $ ./marmoset.py pxe create -l freebsd 3.4.5.6

If the used label has a callback method set that sets a custom root
password for the PXE boot target, you can provide a pasword: 

    $ ./marmoset.py pxe c -l freebsd -p SoSecretPW 3.4.5.6


##### List entries

List all entries:

    $ ./marmoset.py pxe list


##### Remove entries

Remove the entry for an IP address:

    $ ./marmoset.py pxe remove 3.4.5.6


#### VM

##### List VMs

List all defined libvirt domains and their attributes:

    $ ./marmoset.py vm list


### HTTP server

Start it like this:

    $ ./marmoset.py server

Or with gunicorn:
  
    $ gunicorn marmoset.app:app    


#### Routes

##### PXE

List all currently set entries:

    curl -u admin:secret http://localhost:5000/pxe
    #   [
    #     {
    #       "ip_address": "1.2.3.4",
    #       "label": "rescue"
    #     }
    #   ]
    
Create a new PXE config entry. Label defaults to "rescue". If no
password is given, a random password is generated and returned. Takes
JSON Input as well:

    curl -u admin:secret --data 'ip_address=10.10.1.1&label=rescue&password=SeCrEt' \
      http://localhost:5000/pxe
    # 201 on success
    #   {
    #      "ip_address": "10.10.1.1",
    #      "label": "rescue",
    #      "password": "SeCrEt"
    #   }
    #
    # 409 if there is already an entry

Check if there is an entry currently set:

    curl -u admin:secret http://localhost:5000/pxe/10.10.1.1
    # 200 if found
    #   {
    #      "ip_address": "10.10.1.1",
    #      "label": "rescue"
    #   }
    #
    # 404 if not found

Destroy an entry:

    curl -u admin:secret -X DELETE http://localhost:5000/pxe/10.10.1.1
    # 204 on success


##### VM

Create a new VM:

    curl -u admin:secret \
      -d 'name=testvm&user=testuser&ip_address=10.10.1.1&memory=1G&disk=10G' \
      http://localhost:5000/vm
    # 201 on success
    #     {
    #         "disks": [
    #             {
    #                 "bus": "virtio",
    #                 "capacity": "10 GiB",
    #                 "device": "disk",
    #                 "path": "/mnt/data/test-pool/testuser_testvm",
    #                 "target": "hda",
    #                 "type": "block"
    #             }
    #         ],
    #         "interfaces": [
    #             {
    #                 "ip_address": "10.10.1.1",
    #                 "mac_address": "52:54:00:47:b0:09",
    #                 "model": "virtio",
    #                 "network": "default",
    #                 "type": "network"
    #             }
    #         ],
    #         "memory": "1 GiB",
    #         "name": "test",
    #         "state": {
    #             "reason": "unknown",
    #             "state": "shutoff"
    #         },
    #         "user": "testuser",
    #         "uuid": "cd412122-ec04-46d7-ba12-a7757aa5af11",
    #         "vcpu": "1"
    #     }
    # 
    # 422 if there is an error
    #   {"message": "useful error message"}


List all currently defined VMs:

    curl -u admin:secret http://localhost:5000/vm
    # [
    #     {
    #         "disks": [
    #             {
    #                 "bus": "virtio",
    #                 "capacity": "10 GiB",
    #                 "device": "disk",
    #                 "path": "/mnt/data/test-pool/testo",
    #                 "target": "hda",
    #                 "type": "block"
    #             }
    #         ],
    #         "interfaces": [
    #             {
    #                 "ip_address": "10.10.1.1",
    #                 "mac_address": "52:54:00:47:b0:09",
    #                 "model": "virtio",
    #                 "network": "default",
    #                 "type": "network"
    #             }
    #         ],
    #         "memory": "1 GiB",
    #         "name": "test",
    #         "state": {
    #             "reason": "unknown",
    #             "state": "shutoff"
    #         },
    #         "user": "testuser",
    #         "uuid": "cd412122-ec04-46d7-ba12-a7757aa5af11",
    #         "vcpu": "1"
    #     }
    # ]


Get info for a specific VM:

    curl -u admin:secret http://localhost:5000/vm/cd412122-ec04-46d7-ba12-a7757aa5af11
    # 200 on success
    #     {
    #         "disks": [
    #             {
    #                 "bus": "virtio",
    #                 "capacity": "10 GiB",
    #                 "device": "disk",
    #                 "path": "/mnt/data/test-pool/testuser_testvm",
    #                 "target": "hda",
    #                 "type": "block"
    #             }
    #         ],
    #         "interfaces": [
    #             {
    #                 "ip_address": "10.10.1.1",
    #                 "mac_address": "52:54:00:47:b0:09",
    #                 "model": "virtio",
    #                 "network": "default",
    #                 "type": "network"
    #             }
    #         ],
    #         "memory": "1 GiB",
    #         "name": "test",
    #         "state": {
    #             "reason": "unknown",
    #             "state": "shutoff"
    #         },
    #         "user": "testuser",
    #         "uuid": "cd412122-ec04-46d7-ba12-a7757aa5af11",
    #         "vcpu": "1"
    #     }
    # 
    # 404 if the uuid doesn't exist


Remove a VM:

    curl -u admin:secret -X DELETE \
      http://localhost:5000/vm/cd412122-ec04-46d7-ba12-a7757aa5af11
    # 204 on success


## Issues

Find the code at [the git repo](https://www.aibor.de/cgit/marmoset/).

Contact code@aibor.de.



## Copyright

GPLv2 license can be found in LICENSE

Copyright (C) 2015 Tobias Böhm code@aibor.de

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

