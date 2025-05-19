import pytest
import arrow

from csv_transformer.transformers.uuid_to_int_transformer import UUIDToIntTransformer
from csv_transformer.transformers.redact_data_transformer import RedactDataTransformer
from csv_transformer.transformers.format_date_transformer import FormatDatetimeTransformer

def test_uuid_to_int_transformer():
    uuid_to_int_transformer = UUIDToIntTransformer(initial_id = 1)
    uuids = [
        'a1d67e00-5a5d-41e2-91a0-b653531ca831',
        'cc129e10-b095-4753-803a-2bec54348540',
        '46284152-8c5d-4f7b-bd8f-839393a186e1',
    ]
    # in this case, each new int id corresponds to the index of the uuid in the list
    for i, uuid_val in enumerate(uuids):
        int_val = uuid_to_int_transformer.transform(uuid_val)
        assert str(i+1) == int_val


@pytest.mark.parametrize("input",[
    'Hello',
    'bob',
    '123',
    'bob.123@email.com'
])
def test_redact_data_transformer(input: str):
    redact_data_transformer = RedactDataTransformer()
    value = redact_data_transformer.transform(input)
    
    assert len(value) == len(input)

    for i, v in zip(input, value):
        if i.isdigit():
            assert v.isdigit()
        elif i.islower():
            assert v.islower()
        elif i.isupper():
            assert v.isupper()
        elif i.isascii():
            assert v.isascii()


def test_format_datetime():

    def is_valid_datetime(date_string, format_string):
        try:
            arrow.get(date_string, format_string)
            return True
        except Exception:
            return False
        
    input_datetime_format="YYYY-MM-DDTHH:mm:ss"
    output_datetime_format="DD/MM/YYYY"

    format_datetime_transformer = FormatDatetimeTransformer(
        input_datetime_format,
        output_datetime_format
    )
    value = format_datetime_transformer.transform("2025-01-01T12:00:00")
    assert is_valid_datetime(value, output_datetime_format)