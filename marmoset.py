#!/usr/bin/env python3

from argparse import ArgumentParser
from marmoset import config, pxe, virt, webserver

parser   = ArgumentParser(description='Manage libvirt and pxe configs')  
commands = parser.add_subparsers(title='commands')

webserver.subparser.add_to(commands, 'webserver')
pxe.subparser.add_to(commands, 'pxe')
virt.subparser.add_to(commands, 'vm')

args = parser.parse_args()

if 'func' in args:
    args.func(args)
else:
    print('No subcommand given')
    parser.print_help()

