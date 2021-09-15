# Translator Field

The translation service will be essential for standardizing data flowing on the mat. With this service implemented on
the mat, it is possible to state that the data will be treated according to the mat standard.

## Input

The service will receive the data normally, like any other service, and as a configuration, it will receive a
dictionary, containing all field mappings.

```
class ServiceLetter(MatEvent):
    data: dict
    config: ServiceConfig

class ServiceConfig(BaseModel):
    mapping: Dict[str, str] = {}
    preserve_unmapped: bool = True
```

## Output

The output will be a data dictionary, mapped to the fields that came in config.

## Example

```json
//input
{
    "data": {"Name": "foo", "NumberPhone": "000-000"},
    "config": {
        "mapping": {
            "Name": "name",
            "NumberPhone": "phone"
        },
        "preserve_unmapped": true,
    },
}

//output
{
    ...
    "data": {
        "name": "foo",
        "phone": "000-000",
    }
}
```

If ***preserve_unmapped*** is equal to false then the fields unmapped will not be included in the final dict.

```json
//input
{
    "data": {
        "Name": "foo", 
        "NumberPhone": "000-000", 
        "PersonalAdress":"bar"
    },
    "config": {
        "mapping": {
            "Name": "name",
            "NumberPhone": "phone"
        },
        "preserve_unmapped": false,
    },
}

//output
{
    ...
    "data": {
        "name": "foo",
        "phone": "000-000",
    }
}
```