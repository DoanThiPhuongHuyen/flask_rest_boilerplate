import json

from flask import Flask, request
from flask_restplus import Api, Resource, reqparse, fields, marshal

app = Flask(__name__)
api = Api(app, version='1.0', title='Demo flask RESTPlus',
          description='Demo flask RESTPlus',
          )
person_list = {}

model = api.model('Person', {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
})


@api.route('/hello', '/demo')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/hello', '/world')


class PersonDao(object):
    def __init__(self):
        self.counter = 0
        self.person_list = []

    def get(self, id):
        for person in self.person_list:
            if person['id'] == id:
                return person
        api.abort(404, "person {} doesn't exist".format(id))

    def create(self, data):
        person = data
        person['id'] = self.counter = self.counter + 1
        self.person_list.append(person)
        return person

    def update(self, id, data):
        person = self.get(id)
        person.update(data)
        return person

    def delete(self, id):
        person = self.get(id)
        self.person_list.remove(person)


PersonDao = PersonDao()


@api.route('/')
class Person(Resource):
    # envelope keyword argumeent to wrap the resulting output
    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return PersonDao.person_list

    @api.expect(model)
    @api.marshal_with(model, code=201)
    def post(self):
        return PersonDao.create(api.payload), 201


@api.route('/<int:id>')
@api.response(404, 'Todo not found')
@api.param('id', 'The task identifier')
class PersonDetail(Resource):
    @api.doc('get_person')
    @api.marshal_with(model)
    def get(self, id):
        return PersonDao.get(id)

    @api.doc('delete_person')
    @api.response(204, 'Person deleted')
    def delete(self, id):
        PersonDao.delete(id)
        return '', 204

    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
        return PersonDao.update(id, api.payload)


if __name__ == '__main__':
    resource_fields = {'name': fields.String}
    resource_fields['address'] = {}
    resource_fields['address']['line 1'] = fields.String(attribute='addr1')
    resource_fields['address']['line 2'] = fields.String(attribute='addr2')
    resource_fields['address']['city'] = fields.String
    resource_fields['address']['state'] = fields.String
    resource_fields['address']['zip'] = fields.String
    data = {'name': 'bob', 'addr1': '123 fake street', 'addr2': '', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
    print(json.dumps(marshal(data, resource_fields)))
    app.run(debug=True)
