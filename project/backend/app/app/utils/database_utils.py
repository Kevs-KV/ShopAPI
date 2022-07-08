import typing


@typing.no_type_check
def filter_payload(payload):
    return {k: v for k, v in payload.items() if k not in ['cls', 'self'] and v is not None}