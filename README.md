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

### Execution
the `output.csv` file has been created running the following command
```bash
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

## Development

### Running Tests

```bash
pip install -e '.[dev]'
pytest
```

## Notes
- The CLI requires python 3.9 or greater.
- The external library `arrow` has been used to simplify datetime management. It'll be installed in the venv.
- AI agents has been used to assist documentation creation.

## Further improvements

The current implementation loads and transforms the data in one go in memory. Vertical scaling will eventually reach the limit as the nr of rows, columns, and operations increases dramatically.

Pitfalls:
1. Big files with lots of rows and/or columns will waste memory and I/O resources
2. If transformations becomes more complex and are applied to each columns, computational capacity might reach the limit.

therefore further improvements can be considered.

### Vectorized Operations
Use a library like `pandas` in Python to take advantage of vectorized operations. Instead of applying a transformation to each cell individually, row by row, it allows to apply a function to entire columns or rows at once.

Common practice is to load data in chunks instead of full dataset, by setting a fixed nr. of rows for each execution.
Depending on the requirements, either partial success or atomic transformation, the implementation could try to either write the data that was successfully processed or discard the whole output file if even a single row fails.

In addition, boundaries can be set to limit the nr. of rows or file size and columns to prevent too large files to be processed.
This solution improves memory and I/O resource management.

### Multi-threading and multi-processing

To improve further I/O, multi-threading can be used to parallelize data computation tasks while keeping the data to be written in memory. As the chunks of data are processed, the content can be appended to the output file. Threading improve I/O access, although uses same memory and CPU capacity.

If memory and/or CPU become a bottleneck, multiprocessing can be used to effectively create new independent processes, runnning in parallel and having their own memory and cpu capacity. This will increase complexity on how to read and write to the output file. In this case each chunk of data can be passed to an independent process which will write to a temporary csv file. at the end the main task will join the temp files in a single output csv.

## Extending the architecture to a distributed system

### Distributed computation

If transformation logic becomes too complex and CPU intensive, computation could be delegated to external servers. Given the input model, different functions can be implemented as RPC APIs, invoked by the client which will pass the input args in the request. 
Even in this case, the input arguments need to be carefully designed and limited to prevent unbounded requests payloads.

#### Parallelization
As the computation logic is delegated, transformations can be executed in parallel by invoking multiple RPC APIs in parallel. In this case becomes relevant how to manage multi-threading, locking strategies, and call retries. In the latter case, depending on the RPC server SLA, exponential backoff retries or retry-once strategies can be applied. 

**Note:** almost all AWS services implements the "token bucket" retry strategy to prevent retry storms, often caused by exponential backoff strategies, as the service scales up. (https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/).

### Sync vs. Async
As the requirements becomes more and more complex, it should be considered asynchronously processing, maybe storing the file in a cloud storage (i.e.: S3) and process rows as per discussed strategies.
This will increase complexity as state management should be introduced to track processing status.
However the CLI should introduce a new command to retrieve the output file from the remote storage, once processing is completed. 