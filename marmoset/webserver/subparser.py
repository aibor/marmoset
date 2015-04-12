from . import run


def add_to(parser, name):
    command = parser.add_parser(
        name,
        help='start a webserver for API usage',
        aliases=['server'])

    command.set_defaults(func=run)

