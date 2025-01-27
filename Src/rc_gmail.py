# import: std
import os
from time import perf_counter

# import: non-std
from googleapiclient.discovery import build     # type: ignore
from google.oauth2.credentials import Credentials   # type: ignore
from google.auth.transport.requests import Request  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from google.auth.external_account_authorized_user import Credentials as eaau_Credentials # type: ignore
# from googleapiclient.errors import HttpError

# import: local
from rc_logger import logger    # type: ignore
from rc_filter import filter_create, filter_get, filter_list, filter_delete # type: ignore
from rc_message import create_domain_dict, message_modify, messages_list, message_get   # type: ignore
from rc_label import label_create, label_delete, labels_list    # type: ignore

# const/globals
log = logger()

# main


def main():
    # delete_user_labels()
    # delete_domain_filters()
    # populate_domain_labels()
    # populate_domain_filters()
    # update_message_labels(_clean_inbox = True)
    pass

# code blocks


def update_message_labels(_clean_inbox:bool = False) -> None:
    service = gmail_setup()
    label_id_dict = labels_list(service)
    message_ids = {id: thread_id for id, thread_id in messages_list(service)}

    for message_id in message_ids.keys():
        domain_name = message_get(message_id, service)
        if domain_name and label_id_dict:
            domain_name = domain_name.split('.')
            domain_name.reverse()
            domain_name = '/'.join(domain_name)
            label_id_type = label_id_dict.get(domain_name)
            if label_id_type:
                label_id = label_id_type[0]
                # label_type = label_id_type[1]
                log.debug(f'\n\t{message_id=}\n\t{label_id=}')
                message_modify(message_id, label_id, service, _clean_inbox)


def populate_domain_filters() -> None:
    service = gmail_setup()
    label_id_dict = labels_list(service)
    if label_id_dict:
        for label_key in label_id_dict:
            if label_id_dict[label_key][1] == 'user':
                addr_from = label_key.split('/')
                addr_from.reverse()
                addr_from = '.'.join(addr_from)
                addr_from = '*' + addr_from
                label_id = label_id_dict[label_key][0]
                log.debug(f'{label_id=}')
                log.debug(f'{addr_from=}')
                filter_create(service, label_id, addr_from)

def delete_domain_filters() -> None:
    service = gmail_setup()
    f_list = filter_list(service)
    for filters in f_list.values():
        for filter in filters:
            filter_delete(service, filter['id'])



def populate_domain_labels() -> None:
    service = gmail_setup()
    domain_dict = create_domain_dict(service)
    for key in domain_dict:
        label_create(key, service)
        for subkey in domain_dict[key]:
            label_create('/'.join([key, subkey]), service)
            if len(domain_dict[key][subkey]) > 0:
                for item in domain_dict[key][subkey]:
                    label_create('/'.join([key, subkey, item]), service)


def delete_user_labels() -> None:
    service = gmail_setup()
    label_dict = labels_list(service)
    if label_dict:
        for _, value in label_dict.items():
            if value[1] == 'user':
                label_delete(value[0], service)


def gmail_setup() -> Credentials | eaau_Credentials | None:
    # If modifying these scopes, delete the file token.json.
    scopes = ["https://www.googleapis.com/auth/gmail.labels",
              "https://www.googleapis.com/auth/gmail.modify",
              "https://www.googleapis.com/auth/gmail.settings.basic"]
    env_dir = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), '.env')
    cred_path = os.path.join(env_dir, 'credentials.json')
    token_path = os.path.join(env_dir, 'token.json')

    # The file"token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(
            token_path, scopes)
        service = build("gmail", "v1", credentials=creds)
        return service
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            service = build("gmail", "v1", credentials=creds)
            return service
        else:
            if not os.path.exists(cred_path):
                raise RuntimeError("Are credentials.json downloaded into .env?")
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_path, scopes
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, "w") as token:
                token.write(creds.to_json())
        service = build("gmail", "v1", credentials=creds)
        return service
    else:
        return None


if __name__ == '__main__':
    log.debug("Program Start")
    start = perf_counter()
    main()
    log.debug(f"Program Time= {perf_counter() - start:.2f}")
