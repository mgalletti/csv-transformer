from csv_transformer.transformers.uuid_to_int_transformer import UUIDToIntTransformer

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
