# import: std
from time import perf_counter

# import: non-std
from googleapiclient.errors import HttpError

# import: locals
from rc_logger import logger

# globals/const
log = logger()

# main
def main():
    pass

# code blocks

def label_create(_label_name, _service) -> None:
    '''
    name = str()
    label_list_visibility = [labelShow | labelShowIfUnread | labelHide]
    message_list_visibility= [show | hide]
    '''
    label_obj = {'name': _label_name,
                 "labelListVisibility": "labelShowIfUnread",
                 "messageListVisibility": "hide",
                }
    try:
        results = _service.users().labels().create(userId='me', body=label_obj).execute()
        log.debug(f'{results = }')

    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError = }")
    except Exception as _E:
        log.exception(_E.__class__.mro())


def labels_list(_service) -> dict[str,list[str]] | None:
    try:
        # Call the Gmail API
        results = _service.users().labels().list(userId="me").execute()
        # log.debug(f'{results = }')
        # log.debug(f'{type(results) = }')

        labels: list = results.get("labels", [])
        # log.debug(f'{labels = }')
        # log.debug(f'{type(labels) = }')

        if not labels:
        # print("No labels found.")
            return {'empty':[]}

        label_id_dict = {label['name']:[label['id'],label['type']] for label in labels}
        log.debug(f'{label_id_dict}')
        return label_id_dict
    
    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError = }")
    except Exception as _E:
        log.exception(_E.__class__.mro())


def label_delete(_label_id, _service) -> None:
    try:
        results = _service.users().labels().delete(userId='me',id=_label_id).execute()
        log.debug(f'{results = }')

    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError = }")
    except Exception as _E:
        log.exception(_E.__class__.mro())

# logic
if __name__ =='__main__':
    log.debug("Program Start")
    start = perf_counter()
    main()
    log.debug(f"Program Time= {perf_counter() - start:.2f}")