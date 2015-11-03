# JSON Schema in Python

Schema validation and enforcement is a great way to make for compatibles APIs that share a common interchange format.
The existing tooling around JSON schemas is still in it's infancy, the [existing implementations](http://json-schema.org/implementations.html) are too much bound to the implementation details and lack 
flexibility of high level abstraction, so that we optimally write the Python code with data members annotated pretty much like in `Go`  and utilize code & documentation generation to provide both the schemas specification and documentation.
Furthermore, if we carefully decouple the operations, so that we first generate the schema, and then use the schema to generate the documentation we make half of the work *language invariant*. First step on the documentation front would be implementing sensible *Markdown* serializer for the schemas, so we can track them with GitHub.

## Go-like annotations for Python

`Go` allows annotating the source lines with special kind of comments that give hints as to how to `marshal` or `unmarshal` the given source structure via JSON.
Django uses class variables on `Model` classes to do it's [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping). What are the possibilities?

#### `@decorator` way
```python
class Foo(object):
  def __init__(self, bar):
    self._bar = bar
  
  @json.schema(type='string', 
              required=False, 
              desc='bar property of :class:`Foo`')
  @property
  def bar(self):
     return self._bar
```

#### Docstrings annotation

```python
class Foo(object):
  def __init__(self, bar):
    self._bar = bar
  
  @property
  def bar(self):
     """ :json: type='string', required=False, desc='bar property of :class:`Foo`' """
     return self._bar
```

#### ORM-like

```python
class Foo(object):
  bar = schema.Property(type='string', 
                        required=False, 
                        desc='bar property of :class:`Foo`')
                        
  def __init__(self, bar):
    self._bar = bar
  
  @property
  def bar(self):
     return self._bar
```

## Schema generator

Schema generator is an object with rather simplistic interface, you pass in an instance of random object, and it figures out if the object contains proper annotation to perform schema generation.
The output of this operation is either a valid schema or an error / exception that the input object was unfit for schema generation.
This is the place where most of the above annotation logic will get interpreted - all 3 ways are conceptually very similar, yet differ in rather subtle ways:

  * The Docstring way will not work for optimized builds, where Docstrings are stripped
  * The decorator way incurs runtime penalty for each annotated function call
  * The ORM-like way induces constraints on naming and class variables
  
The ORM-like way seems to be a winner because the schemas will be for major part handled by machines, and all human interjection needed should be simply defining the class variables.
The definition for the ORM-like way could be collated into a single variable to fix the naming issues:

```python
class Foo(object):
  _json_schema = json.Schema(schema.Property(type='string', 
                                             required=False, 
                                             desc='bar property of :class:`Foo`'))
                        
  def __init__(self, bar):
    self._bar = bar
  
  @property
  def bar(self):
     return self._bar
```

The other benefit of this solution is that we could, for most part, simply use [jsl](https://github.com/aromanovich/jsl) which is a Python DSL for JSON schemas.
Inheritance is used to establish relations on a parent-child basis, might be worthwhile to also explore and figure out how to support other patterns like composition, to decouple the marshalling functionality from the objects themselves.
Another consideration is whether to get rid of the common base class `jsl.Document` and move the funcionality to the Schema Generator or accept `jsl.Document` as root of our object hierarchy and get rid of the Schema Generator.
