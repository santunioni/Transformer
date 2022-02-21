# JSON Transformer

A JSON to JSON Transformer.

The JSON Transformer Service allows the transformation of JSONs used in another services. Current added functionalities
are:

- Map Keys
- Delete Keys
- Aggregate Key-values in another keys.
- Add Key-value pairs.
- Sanitize Values.

## Input

The service will receive the data normally, like any other service, also it receives a configuration containing the
selected transformations and its specific configurations.

## Output

The Transformed JSON with all transformations performed.

## Transformers

### MapKeys

The MapKeys is a complete dict re-designer. It lets you rename the keys and also restructure the entire dict. Creating
new nested data where there wasn't and also flattening data that was previously nested is possible, all that preserving
the data from the input dictionary.

#### Instructions to set mapping configuration:

The mapping is a JSON. On the key side of the mapping you put the nested path of the key you want. A nested path is for
example. A value inside key_1 inside the first index of a list, inside another dictc in key_2 has the
path: ```key_2[1].key_1```
On the value side you put the nested path of where the value get in the key side in the data will be mapped. Look at the
example for more information.

- The placeholder "@{}" is used to get value inside the metadata. You need to put the key inside the placeholder.
- The placeholder "[]" is used to map the data into a specific index in the list. You need to put the index inside the
  placeholder.
- The nested path is written with the keys and indexes separated by "."

#### Example:

```python
# The input including data and metadata
input_metadata = {
    "type": "deal",
    "origin": "pipedrive"
}
input_data = {
    "id": 1645687,
    "cliente": {
        "nome": "Marli Aparecida Ana das Neves",
        "email": "marliaparecidaanadasneves-77@mail.com"
    }}

# the mapping configuration
mapping = {
    "id": "@{origin}_@{type}_id",
    "cliente.nome": "client.name",
    "client.email": "emails[0]",
}

# The output after the transformer.
output_data = {
    "id": "deal_pipedrive_id",
    "client": {"name": "Marli Aparecida Ana das Neves"},
    "emails": ["marliaparecidaanadasneves-77@mail.com"]
}
```

### AddKeys

This Transform is able to add key-value pairs to the data. The pairs are passed inside a dict and they will be
incorporated into the data. The non triviality of this transform comes from the possibility of passing pairs that uses
values of other pairs in the existing data or metadata.

Only keys that map to string can be passed. The strings are passed with .lower() method.

#### For Example:

```python
# The input 
data = {'data_key_1': 'data_value_1'}
metadata = {'meta_1': 'meta_value_1'}

# The configuration
key_values = {
    'key_2': 'value_2',
    'new_key_${data_key_1}': "${data_key_1}_@{meta_1}"
}

# The Transformed output will be:
output = {
    'data_key_1': 'data_value_1',
    'key_2': 'value_2',
    'new_key_data_value_1': "data_value_1_meta_value_1"
}
```

### DeleteKeys

This simply delete key-value pairs from the data dict. Its possible to specify the keys directly or to pass a Regular
Expression (RegEx), every key that is a complete match to the RegEx will be deleted. Both can be used at the same time.

### SanitizeValues

Use key-pattern to select all keys that is a fullmatch to a RegEx pattern. The sub-pattern is used to select parts of
the values that should be substituted by the sub_string. The string methods are the names of builtin python string
methods

#### Example

This is cpf mask remover:

```python
# input
data = {"cpf": "123.456.789-01"}

# configuration
key_pattern = "cpf"
sub_pattern = "[^0-9]"

# output
output = {"cpf": "12345678901"}
```

### AggregateKeys

This transform is responsible for aggregating data. Pass a list of keys or a RegEx pattern and the keys will be stored
inside a list in a new_key. Both pattern and Keys list can be used at the same time.

```python
pattern = "^(email_).*"
# or
keys = ['email_1', 'email_2', 'email_3']

# turns this:
data = {
    "email_1": "a@g.com",
    "email_2": "b@g.com",
    "email_3": "c@g.com"
}

# into this:

output = {
    "emails": ["a@g.com", "b@g.com", "c@g.com"]
}
```
