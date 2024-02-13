# import: std
from time import perf_counter
from typing import Generator, Any

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


def message_get(_message_id, _service) -> None | str:
    try:
        result = _service.users().messages().get(userId='me', id=_message_id).execute()
        # log.debug(f'{result = }')
        if not result.get('payload'):
            log.error(f'No payload for {_message_id}')
            return 'error0'
        result = result.get('payload')
        result = result.get('headers')
        for header in result:
            if header['name'] == 'From':
                address = header['value']
                address = address.split('@')
                domain: str = address[-1].rstrip('>')
                return domain

    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError=}")
    except Exception as _E:
        log.exception(_E.__class__.mro())


def messages_list(_service) -> Generator[Any, Any, Any]:
    try:
        def list_generator(_maxResults=499, _pageToken=None):
            results = _service.users().messages().list(
                userId='me', maxResults=_maxResults, pageToken=_pageToken).execute()
            if len(results['messages']) < _maxResults:
                return
            # log.debug(f'{results = }')
            yield results['messages']
            next_page_token = results.get('nextPageToken')
            # log.debug(f'{next_page_token = }')
            for next_results in list_generator(_maxResults, next_page_token):
                yield next_results

        for results in list_generator():
            for result in results:
                # log.debug(f'{result = }')
                id = result['id']
                threadid = result['threadId']
                yield (id, threadid)

    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError=}")
    except Exception as _E:
        log.exception(_E.__class__.mro())


def message_modify(_message_id, _label_id, _service, _clean_inbox:bool = False):
    label_obj = {
        "addLabelIds": [_label_id],
        "removeLabelIds": []
    }
    if _clean_inbox:
        label_obj['removeLabelIds'].append('inbox')
    try:
        result = _service.users().messages().modify(
            userId='me', id=_message_id, body=label_obj).execute()
        log.debug(f'{result=}')

    except HttpError as _HttpError:
        # TODO(developer) - Handle errors from gmail API.
        log.exception(f" {_HttpError=}")
    except Exception as _E:
        log.exception(_E.__class__.mro())


def create_domain_dict(_service) -> dict:
    message_ids = {id: thread_id for id, thread_id in messages_list(_service)}
    log.debug(f'{len(message_ids)=}')
    domain_dict = {}
    for message_id in message_ids.keys():
        result = message_get(message_id, _service)
        if result:
            domain_parts = result.split('.')
            domain_parts.reverse()
            if not domain_dict.get(domain_parts[0]):
                domain_dict[domain_parts[0]] = dict()
            domain_dict[domain_parts[0]].update(
                {domain_parts[1]: domain_parts[2:]})
    log.debug(domain_dict)
    return domain_dict


# logic
if __name__ == '__main__':
    log.debug("Program Start")
    start = perf_counter()
    main()
    log.debug(f"Program Time= {perf_counter() - start:.2f}")
