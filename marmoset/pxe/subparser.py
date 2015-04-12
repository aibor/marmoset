from . import Label, ClientConfig


def create(args):
    pxe_client = ClientConfig(args.ip_address, args.password)
    pxe_client.create(Label.find(args.label))
    msg = 'Created %s with password %s' 
    print(msg % (pxe_client.file_path(), pxe_client.password))


def list(args):
    for pxe_client in ClientConfig.all():
        print('%s: %s' % (pxe_client.ip_address, pxe_client.label))


def remove(args):
    pxe_client = ClientConfig(args.ip_address)
    if pxe_client.remove():
        print('Removed', pxe_client.file_path())
    else:
        print('No entry found for', pxe_client.ip_address)


def add_to(parser, name):
    command = parser.add_parser(name,
            help='manage client specific PXE configs'
            )

    subcommands = command.add_subparsers(title='pxe subcommands')

    pxe_create = subcommands.add_parser('create',
        help='Create a PXE config for an IP address.',
        aliases=['c', 'add'])
    pxe_create.add_argument('ip_address',
        help='IP address to create PXE entry for')
    pxe_create.add_argument('-l', '--label',
        help='the PXE label to set',
        choices=Label.names(),
        default=Label.names()[0])
    pxe_create.add_argument('-p', '--password',
        help='''Password which is set as the root password if the chosen label
        supports this. If a password is necessary for the choosen label and
        none is given random password is created and returned''',
        default=None)
    pxe_create.set_defaults(func=create)

    pxe_list = subcommands.add_parser('list',
        help='list IP addresses for all currently present PXE client config',
        aliases=['l'])
    pxe_list.set_defaults(func=list)

    pxe_remove = subcommands.add_parser('remove',
        help='remove a PXE config for an IP address',
        aliases=['r', 'rem', 'd', 'del'])
    pxe_remove.add_argument('ip_address', help='IP address to remove PXE entry for')
    pxe_remove.set_defaults(func=remove)

