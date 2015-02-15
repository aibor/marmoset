#!/usr/bin/env python3

from lib.pxe_client_config import PXEClientConfig
import argparse

parser = argparse.ArgumentParser(description='Manage client specific PXE configs')
parser.add_argument('command', help='subcommand to process', choices=['create', 'remove'])
parser.add_argument('ip_address', help='IP address to create/remove PXE entry for')

args = parser.parse_args()

pxe_client = PXEClientConfig(args.ip_address)

print(getattr(pxe_client, args.command)())

