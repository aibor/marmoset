#!/usr/bin/env python3

from marmoset.pxe_client_config import PXEClientConfig, Template
from marmoset.webserver import webserver
from os import listdir, system
import argparse, sys, configparser

try:
    import settings
    if 'CFG_DIR' in vars(settings):
        PXEClientConfig.CFG_DIR = settings.CFG_DIR
    if 'TEMPLATES' in vars(settings):
        [Template(x, settings.TEMPLATES[x]) for x in settings.TEMPLATES]
except Exception as e:
    print("Warning: ", e)


def run_webserver(args):
    webserver.run()


def create(args):
    pxe_client = PXEClientConfig(args.ip_address)
    entryfile = pxe_client.create(args.template)
    print('Created', entryfile)
    if 'callback' in args and args.callback:
        system('{} {} {} {}'.format(args.callback, args.template,
            pxe_client.ip_address, entryfile))


def list(args):
    for pxe_client in PXEClientConfig.all():
        print(pxe_client.ip_address)


def remove(args):
    pxe_client = PXEClientConfig(args.ip_address)
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
        help='create a PXE config for an IP address',
        aliases=['c', 'add'])
pxe_create.add_argument('ip_address',
        help='IP address to create PXE entry for')
pxe_create.add_argument('-t', '--template',
        help='the PXE config template to use',
        choices=Template.all(),
        default='rescue')
pxe_create.add_argument('-c', '--callback',
        help='name or path of an executable file that is called after the '
        'entry has been created with name of template and ip as arguments')
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

