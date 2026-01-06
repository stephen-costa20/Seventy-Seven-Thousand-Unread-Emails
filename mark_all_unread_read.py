import os
import time
import random
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Needs modify scope to remove the UNREAD label.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

# Gmail API allows batchModify with up to 1000 message IDs per call.
BATCH_SIZE = 1000


def get_gmail_service():
    """
    Authenticates with OAuth and returns a Gmail API service client.
    Stores/reads OAuth tokens from token.json for reuse.
    """
    creds: Optional[Credentials] = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Missing {CREDENTIALS_FILE}. Download OAuth client JSON and save it as {CREDENTIALS_FILE}."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            # Opens browser for consent; local server receives the auth code.
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def list_message_ids(service, user_id: str, query: str) -> List[str]:
    """
    Lists message IDs matching the Gmail search query (supports 'is:unread', etc.).
    Uses pagination until all matching messages are retrieved.
    """
    message_ids: List[str] = []
    page_token: Optional[str] = None

    while True:
        resp = (
            service.users()
            .messages()
            .list(userId=user_id, q=query, pageToken=page_token, maxResults=500)
            .execute()
        )

        msgs = resp.get("messages", [])
        if msgs:
            message_ids.extend(m["id"] for m in msgs)

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return message_ids


def chunks(lst: List[str], n: int):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def with_retries(fn, max_retries: int = 8):
    """
    Retries transient Gmail API failures (429, 500, 503) with exponential backoff + jitter.
    """
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except HttpError as e:
            status = getattr(e.resp, "status", None)
            # Rate limit / transient backend errors
            if status in (429, 500, 503):
                if attempt == max_retries:
                    raise
                sleep_s = min(2 ** attempt, 60) + random.random()
                print(f"Transient error HTTP {status}. Retrying in {sleep_s:.1f}s...")
                time.sleep(sleep_s)
                continue
            raise


def mark_ids_as_read(service, user_id: str, message_ids: List[str]) -> None:
    """
    Removes the UNREAD label from the provided message IDs in batches.
    """
    total = len(message_ids)
    if total == 0:
        print("No matching messages found.")
        return

    processed = 0
    for batch in chunks(message_ids, BATCH_SIZE):
        body = {"ids": batch, "removeLabelIds": ["UNREAD"]}

        def _do():
            return service.users().messages().batchModify(userId=user_id, body=body).execute()

        with_retries(_do)
        processed += len(batch)
        print(f"Marked as read: {processed}/{total}")


def main():
    user_id = "me"

    # Choose ONE:
    # 1) Unread in standard searchable locations (common default):
    query = "is:unread"
    # 2) If you truly want absolutely everywhere (including spam/trash), try:
    # query = "is:unread in:anywhere"

    service = get_gmail_service()
    print(f"Searching for unread messages with query: {query!r} ...")
    ids = list_message_ids(service, user_id=user_id, query=query)
    print(f"Found {len(ids)} unread messages. Marking as read in batches...")
    mark_ids_as_read(service, user_id=user_id, message_ids=ids)
    print("Done.")


if __name__ == "__main__":
    main()