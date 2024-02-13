# import: std
import os
from time import perf_counter

# import: non-std
from googleapiclient.errors import HttpError

# import: local
from rc_logger import logger

# const/globals
log = logger()

# main
def main():
    pass


# code blocks
def filter_create(_service, _label_id, _target_from):

    filter_obj = {"action": {"addLabelIds": [_label_id]},"criteria": {"from": _target_from}}
    try:
        result = _service.users().settings().filters().create(userId='me',body = filter_obj).execute()
        log.debug(f'{result = }')

    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError = }")
    except Exception as _E:
        log.exception(_E.__class__.mro())
    pass


if __name__ == '__main__':
    log.debug("Program Start")
    start = perf_counter()
    main()
    log.debug(f"Program Time= {perf_counter() - start:.2f}")