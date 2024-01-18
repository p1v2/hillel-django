from django.contrib.auth.models import User

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_sheets_service(user: User):
    token = user.socialaccount_set.get(provider="google").socialtoken_set.get().token
    refresh_token = user.socialaccount_set.get(provider="google").socialtoken_set.get().token_secret

    credentials = Credentials(
        token=token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    service = build("sheets", "v4", credentials=credentials)

    return service


def write_to_google_sheet(user: User):
    service = get_sheets_service(user)
    sheet = service.spreadsheets()
    sheet.values().update(
        spreadsheetId="1XowHPfR2qmPs5ejHbmvV_UxzFHy49FzCUTSHQTBnMnc",
        range="A:Z",
        valueInputOption="USER_ENTERED",
        body={
            "values": [
                ["Hello", "World"]
            ]
        }
    ).execute()
