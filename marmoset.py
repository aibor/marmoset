#!/usr/bin/env python3

from argparse import ArgumentParser
from marmoset import config, webserver

def show_config(*args):
    with open('/dev/stdout', 'w') as stdout:
        config.write(stdout)

parser   = ArgumentParser(description='Manage libvirt and pxe configs')  
commands = parser.add_subparsers(title='commands')


config_cmd = commands.add_parser('config', help='show config directives used')
config_cmd.set_defaults(func=show_config)


webserver.subparser.add_to(commands,
    'webserver',
    help='start a webserver for API usage',
    aliases=['server']
)

if config['Modules'].getboolean('PXE'):
    from marmoset import pxe

    pxe.subparser.add_to(commands,
        'pxe',
        help='manage client specific PXE configs'
    ) 

if config['Modules'].getboolean('VM'):
    from marmoset import virt

    virt.subparser.add_to(commands,
        'vm',
        help='manage libvirt domains and their associated resources'
    )


args = parser.parse_args()

if 'func' in args:
    args.func(args)
else:
    print('No subcommand given')
    parser.print_help()

