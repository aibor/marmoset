from flask import request
from flask.ext.restful import reqparse, Resource, url_for, abort
from werkzeug.exceptions import NotFound
from marmoset import virt


parser = reqparse.RequestParser()
parser.add_argument('user', type=str, required=True)
parser.add_argument('name', type=str, required=True)
parser.add_argument('memory', type=int, required=True)
parser.add_argument('cpu', type=int, default=1)
parser.add_argument('disk', type=int, required=True)

command_parser = reqparse.RequestParser()
command_parser.add_argument('command', type=str, required=True,
        choices=['start', 'stop', 'shutdown', 'reset'])
command_parser.add_argument('params', type=str, action='append', default=[])


def find_domain(uuid):
    domain = virt.Domain.find_by('uuid', uuid)
    if domain is None:
        abort(404)
    else:
        return domain


class VMCollection(Resource):

    def get(self):
        domains = virt.Domain.all()
        return [d.attributes() for d in domains]

    def post(self):
        pass


class VMObject(Resource):

    def get(self, uuid):
        return find_domain(uuid).attributes()

    def put(self, uuid):
        pass

    def delete(self, uuid):
        pass


class VMCommand(Resource):

    def put(self, uuid):
        args = command_parser.parse_args() 
        print(args)
        domain = find_domain(uuid)
        try:
            res = getattr(domain, args['command'])(*args['params'])
            return ('', 204) if not res else (res, 200)
        except Exception as e:
            abort(422, message = str(e))

