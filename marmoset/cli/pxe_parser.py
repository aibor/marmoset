from .. import pxe


def add_to(parser, name, **kwargs):
    command     = parser.add_parser(name, **kwargs)
    subcommands = command.add_subparsers(title='%s subcommands' % name)

    pxe_create = subcommands.add_parser('create',
        help='Create a PXE config for an IP address.',
        aliases=['c', 'add'])
    pxe_create.set_defaults(func=pxe.create)
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
    pxe_create.add_argument('-s', '--script',
                            help='''Sciptfilepath''',
                            default=None)

    pxe_list = subcommands.add_parser('list',
        help='list IP addresses for all currently present PXE client config',
        aliases=['l'])
    pxe_list.set_defaults(func=pxe.list)

    pxe_remove = subcommands.add_parser('remove',
        help='remove a PXE config for an IP address',
        aliases=['r', 'delete', 'del', 'd'])
    pxe_remove.set_defaults(func=pxe.remove)
    pxe_remove.add_argument('ip_address', help='IP address to remove PXE entry for')

