general_query = '''
query {
  __schema {
    types {
      name
      description
      kind
    }
    queryType{
      name
      fields {
        name
        description
				args {
          name
				  description
          type {
            name
          }
				}
        type {
          name
          description
        }
      }
    }
    mutationType{
      name
      fields {
        name
        description
				args {
          name
				  description
          type {
            name
          }
				}
        type {
          name
          description
        }
      }
    }
  }
}
'''

schema_query = '''
query {
  __schema {
    types {
      name
      description
      kind
    }
  }
}
'''

type_query = '''
query t {
  __type(name: "@TYPE_NAME") {
    kind
    name
    description
    fields {
      name
      description
      type {
        name
        description
      }
      args {
        name
        description
        type {
          name
        }
      }
    }
    inputFields {
      name
      description
      type {
        name
      }
    }
    interfaces {
      name
      description
    }
    possibleTypes {
      name
      description
    }
  }
}
'''

def get_query(_type, name=None):
    if _type == 'schema':
        return schema_query
    if _type == 'general':
        return general_query
    if _type == 'type':
        return type_query.replace('@TYPE_NAME', name)