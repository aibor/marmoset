#!/usr/bin/env python3

from lib.pxe_client_config import PXEClientConfig
from os import listdir, system
import argparse
try:
    import settings
except: pass


if 'settings' in globals() and 'CFG_DIR' in vars(settings):
    PXEClientConfig.CFG_DIR = settings.CFG_DIR


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
    print(pxe_client.remove())


parser = argparse.ArgumentParser(description='Manage client specific PXE configs')
subparsers = parser.add_subparsers(title='subcommands')


parser_create = subparsers.add_parser('create',
        help='create a PXE config for an IP address',
        aliases=['c', 'add'])
parser_create.add_argument('ip_address',
        help='IP address to create PXE entry for')
parser_create.add_argument('-t', '--template',
        help='the PXE config template to use',
        choices=listdir(PXEClientConfig.TMPL_DIR),
        default='rescue')
parser_create.add_argument('-c', '--callback',
        help='name or path of an executable file that is called after the '
        'entry has been created with name of template and ip as arguments')
parser_create.set_defaults(func=create)


parser_list = subparsers.add_parser('list',
        help='list IP addresses for all currently present PXE client config',
        aliases=['l'])
parser_list.set_defaults(func=list)


parser_remove = subparsers.add_parser('remove',
        help='remove a PXE config for an IP address',
        aliases=['r', 'rem', 'd', 'del'])
parser_remove.add_argument('ip_address', help='IP address to remove PXE entry for')
parser_remove.set_defaults(func=remove)

args = parser.parse_args()

if 'func' in args:
    args.func(args)
else:
    print('No subcommand given')
    parser.print_help()

