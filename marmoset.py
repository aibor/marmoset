#!/usr/bin/env python3

from os import listdir, system
import argparse, sys, configparser
from marmoset import pxe, virt

config = configparser.ConfigParser()

config['Webserver'] = {'Username': 'admin', 'Password': 'secret'}
config['PXEConfig'] = {'ConfigDirectory': '/srv/tftp/pxelinux.cfg'}
config['PXELabel']  = {}
config['Libvirt']   = {'URI': 'qemu:///system'}

config.read('marmoset.conf')

if config.options('PXELabel').__len__() == 0:
    raise Exception('No PXELabel defined in config')

# Create pxe label list.
[pxe.Label(n, cb) for n, cb in config['PXELabel'].items()]

pxe.ClientConfig.CFG_DIR = config['PXEConfig']['ConfigDirectory']

virt.virt.URI = config['Libvirt']['URI']


def run_webserver(args):
    from marmoset import webserver
    webserver.auth.Username  = config['Webserver']['Username']
    webserver.auth.Password  = config['Webserver']['Password']
    webserver.app.run()


def create(args):
    pxe_client = pxe.ClientConfig(args.ip_address, args.password)
    pxe_client.create(pxe.Label.find(args.label))
    msg = 'Created %s with password %s' 
    print(msg % (pxe_client.file_path(), pxe_client.password))


def list(args):
    for pxe_client in pxe.ClientConfig.all():
        print('%s: %s' % (pxe_client.ip_address, pxe_client.label))


def remove(args):
    pxe_client = pxe.ClientConfig(args.ip_address)
    if pxe_client.remove():
        print('Removed', pxe_client.file_path())
    else:
        print('No entry found for', pxe_client.ip_address)


parser = argparse.ArgumentParser(description='Manage client specific PXE configs')

commands = parser.add_subparsers(title='commands')


command_webserver = commands.add_parser('webserver',
        help='start a webserver for API usage',
        aliases=['server'])
command_webserver.set_defaults(func=run_webserver)


command_pxe = commands.add_parser('pxe',
        help='manage client specific PXE configs',
        aliases=['pxe'])


subcommands_pxe = command_pxe.add_subparsers(title='pxe subcommands')

pxe_create = subcommands_pxe.add_parser('create',
        help='Create a PXE config for an IP address.',
        aliases=['c', 'add'])
pxe_create.add_argument('ip_address',
        help='IP address to create PXE entry for')
pxe_create.add_argument('-l', '--label',
        help='the PXE label to set',
        choices=pxe.Label.names(),
        default=pxe.Label.names()[0])
pxe_create.add_argument('-p', '--password',
        help='''Password which is set as the root password if the chosen label
        supports this. If a password is necessary for the choosen label and
        none is given random password is created and returned''',
        default=None)
pxe_create.set_defaults(func=create)


pxe_list = subcommands_pxe.add_parser('list',
        help='list IP addresses for all currently present PXE client config',
        aliases=['l'])
pxe_list.set_defaults(func=list)


pxe_remove = subcommands_pxe.add_parser('remove',
        help='remove a PXE config for an IP address',
        aliases=['r', 'rem', 'd', 'del'])
pxe_remove.add_argument('ip_address', help='IP address to remove PXE entry for')
pxe_remove.set_defaults(func=remove)


args = parser.parse_args()


if 'func' in args:
    args.func(args)
else:
    print('No subcommand given')
    parser.print_help()

