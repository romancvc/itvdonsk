import asyncio
import uuid
from datetime import datetime
import asyncpg


next_numb = ''

async def run_connect():
    global conn
    conn = await asyncpg.connect(user='postgres', password='21761815',
                                 database='itvdonsk', host='127.0.0.1', port='5432')
    return conn


async def event_numb_generator():
    global next_numb
    await run_connect()
    events = await conn.fetch(f"SELECT event_number FROM tgbot_tgevent")
    base_numb = 1
    for numb in events:
        ev_num = str(numb).split("'")
        int_numb = ev_num[1].split("-")
        if int(int_numb[1]) > base_numb:
            base_numb = int(int_numb[1])
    base_numb = base_numb + 1
    next_numb = 'БР-000' + str(base_numb)
    return next_numb


async def cmd_start_db(chat_id, username):
    await run_connect()
    all_users = await conn.fetch(f'SELECT external_id FROM tgbot_tguser')
    if str(chat_id) in str(all_users):
        return False
    else:
        await conn.execute(f"INSERT INTO tgbot_tguser (external_id,nickname) VALUES ({str(chat_id)},'{str(username)}')")
        return True


async def check_authorization_bd(chat_id):
    await run_connect()
    check = await conn.fetchval(f"SELECT company_id FROM tgbot_tguser WHERE external_id='{str(chat_id)}'")
    if check is None:
        return False
    else:
        return True


async def process_authorization_db(text, chat_id):
    await run_connect()
    all_passwords = await conn.fetch(f"SELECT tg_password FROM data_one_c_client")
    if str(text) in str(all_passwords):
        this_company = await conn.fetchval(f"SELECT full_name FROM data_one_c_client WHERE tg_password='{str(text)}'")
        await conn.execute(f"UPDATE tgbot_tguser SET company_id=(SELECT id FROM data_one_c_client WHERE "
                           f"tg_password='{str(text)}') WHERE external_id='{str(chat_id)}'")
        return this_company


async def voice_to_text_db(chat_id, text, name_and_number):
    await run_connect()
    zero_client = await conn.fetchval(f"SELECT id FROM data_one_c_client WHERE full_name='Пустой контрагент'")
    this_client = await conn.fetchval(f"SELECT company_id FROM tgbot_tguser WHERE external_id='{str(chat_id)}'")
    if this_client is None:
        await conn.execute(f"INSERT INTO tgbot_tgevent VALUES ('{uuid.uuid4()}','{await event_numb_generator()}',"
                           f"'{datetime.now()}','Заявка из телеграма {await event_numb_generator()}','{name_and_number}. {text}', "
                           f"(SELECT id FROM data_one_c_client WHERE full_name='Пустой контрагент'))")
        this_event = await conn.fetchval(f"SELECT event_number FROM tgbot_tgevent WHERE event_number='{str(next_numb)}'")
        return this_event
    else:
        await conn.execute(f"INSERT INTO tgbot_tgevent VALUES ('{uuid.uuid4()}','{await event_numb_generator()}',"
                           f"'{datetime.now()}','Заявка из телеграма {await event_numb_generator()}','{text}', "
                           f"(SELECT company_id FROM tgbot_tguser WHERE external_id='{str(chat_id)}'))")
        this_event = await conn.fetchval(f"SELECT event_number FROM tgbot_tgevent WHERE event_number='{str(next_numb)}'")
        return this_event

async def get_number_tgevent():
    await run_connect()

