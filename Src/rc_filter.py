# import: std
import os
from time import perf_counter

# import: non-std
from googleapiclient.errors import HttpError    # type: ignore

# import: local
from rc_logger import logger    # type: ignore

# const/globals
log = logger()

# main
def main():
    pass


# code blocks

def filter_get(_service,_filter_id):
    try:
        result = _service.users().settings().filters().get(userId='me',id=_filter_id).execute()
        log.debug(f'{result = }')

    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError = }")
    except Exception as _E:
        log.exception(_E.__class__.mro())

def filter_list(_service):
    try:
        result = _service.users().settings().filters().list(userId='me').execute()
        log.debug(f'{result = }')
    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError = }")
    except Exception as _E:
        log.exception(_E.__class__.mro())
    return result

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

def filter_delete(_service, _filter_id):
    try:
        result = _service.users().settings().filters().delete(userId='me',id=_filter_id).execute()
        log.debug(f'{result = }')

    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError = }")
    except Exception as _E:
        log.exception(_E.__class__.mro())


if __name__ == '__main__':
    log.debug("Program Start")
    start = perf_counter()
    main()
    log.debug(f"Program Time= {perf_counter() - start:.2f}")