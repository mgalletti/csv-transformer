# CSV Transformer

A Python command line application that allows a user to transform an existing dataset into a dataset with a different format.

## Installation

Create a virtual env and install necessary dependencies

```bash
# create virtual env
python -m venv .venv
# activate venv
source .venv/bin/activate
# install package
pip install -e .
```

Once installed, you can use the cli by invoking the command `csv-transform`

To exit package execution scope, deactivate the virtual env
```bash
# deactivate virtual env
deactivate
```

## Usage

The cli script takes several parameters as input. The first and second must be the relative file path to the input and output csv file respectively.
The following parameter must be the definition of the transformation you want to perform on the input file data

CLI help gives details about each parameter

```bash
csv-transform "<path to input csv>" "<path to output csv>" -t "<transformers definition> OR <path to definition>"

# run help
csv-transform -h
```

The transformation definition can be passed inline as escaped JSON or as a path to the JSON file.

Example:
```bash
# inline JSON
csv-transform data/user_sample.csv data/output.csv -t "{\"transfomers\":{\"uuid_to_int\":[{\"column_name\":\"user_id\",\"transformer_args\":{\"initial_id\":1}}]},\"column_order\":[\"manager_id\",\"start_date\",\"user_id\",\"name\",\"email_address\",\"last_login\"]}"
# file path
csv-transform data/user_sample.csv data/output.csv -t data/transformation_definition.json
```

## Transformation definition Model

Transformations follow this model:

```
{
  "transfomers":{
    "<transformer_name>": [{
      "column_name": <column_name>,
      "transformer_args": <JSON object with input args>
    }]
  },
  "column_order": [<column_name>, ...]
}
```

**`transfomers` (required)** list of transformation to apply to csv fields
- `transformer_name` (str, required): Name of the transformer to apply. The value of this attribute is a list of JSON objects specifying for which columns the same transformation should be applied, with the proper instructions
- `column_name` (str, required): This parameter is required for all transformations to specify which column to transform
- `args` (dict, required): JSON object that defines the input arguments of the transformer. The arguments don't follow a predefined schema and depends on each transformer.

**`column_order` (optional):**: List of fields names that defines how column should be ordered in the output file. It's an optional attribute, although if provided it must list all fields in the csv, otherwise it'll raise a `ValueError`.


Example:
```
{
  "transfomers": {
    "uuid_to_int": [{
      "column_name": "user_id",
      "transformer_args": {
        "initial_id": 1
      }
    }]
  },
  "column_order": [
    "manager_id",
    "start_date",
    "user_id",
    "name",
    "email_address",
    "last_login"
  ]
}
```

You can think of this model as a set of RPC API interfaces where <transformer_name> is the procedure name, while the list of JSON object is the request payload

### Available Transformers

#### `uuid_to_int`

Convert UUIDs into a simple integer sequence, whilst maintaining their uniqueness.

Arguments:
- `initial_id` (int, optiona): the integer that sets the id to start from (default: 0)

#### `format_date`

Formats dates according to specified format

Arguments:
  - `input_datetime_format` (str, optional): the datetime format string of the input value (default: 'YYYY-MM-DD')
  - `output_datetime_format` (str, optional): the datetime format string of the output value (default: 'YYYY-MM-DD')

#### `redact_data`

Redacts sensitive data and replace it with similar looking random data. The new string preserve case-format (lower, upper) and digits types. 
Other ASCII characters (i.e.: punctuation) are left as is.

Arguments: 
At the moment no arguments is required, although the `args` attribute must always be defined.

### Multiple fields transformations

The JSON object can specify multiple transformers.

Example:
```
{
  "transfomers": {
    "uuid_to_int": [{
      "column_name": "user_id",
      "transformer_args": {
        "initial_id": 1
      }
    },{
      "column_name": "manager_id",
      "transformer_args": {
        "initial_id": 0
      }
    }],
    "redact_data": [{
      "column_name": "name",
      "transformer_args": {}
    }]
  }
}
```