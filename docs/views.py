from django.shortcuts import render
from gql import Client, gql

from hackernews.schema import schema
from .query import get_query

# Create your views here.
client = Client(schema=schema)
query = gql(get_query(_type='general'))
result_schema = client.execute(query)

types = result_schema['__schema']['types']
data = {}
for i in types:
    kind = i['kind']
    name = i['name']
    if data.get(kind):
        data[kind].append(name)
    else:
        data[kind] = [name]

def index(request):
    # query = gql(get_query(_type='schema'))
    # result = client.execute(query)


    context = {'schema': result_schema['__schema'], 'menu': data}
    return render(request, 'index.html', context)

def detail(request, name):
    query = gql(get_query(name=name, _type='type'))
    result = client.execute(query)
    
    foo = result['__type']
    # caso seja um objeto
    query_fields = result_schema['__schema']['queryType']['fields']
    mutation_fields = result_schema['__schema']['mutationType']['fields']
    if not result['__type']:
        for field in query_fields:
            if name == field['name']:
                foo = field
        if not foo:
            for field in mutation_fields:
                if name == field['name']:
                    foo = field

    context = {'schema': result_schema['__schema'], 'foo': foo, 'menu': data}
    return render(request, 'index.html', context)
