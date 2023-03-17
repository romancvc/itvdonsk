from asgiref.sync import sync_to_async

from data_one_c.models import Client
from tgbot.models import TgUser


@sync_to_async
def process_authorization_all_passwords_sync():
    result = Client.objects.values_list('tg_password', flat=True)
    print(result)
    return result


@sync_to_async
def process_authorization_this_company_sync(text):
    result = Client.objects.values_list('id', flat=True).get(tg_password=text)
    print(result)
    return result


@sync_to_async
def process_authorization_sync(chat_id, this_company):
    TgUser.objects.filter(external_id=chat_id).update(company=this_company)