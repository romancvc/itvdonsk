from tgbot.models import TgEvent


def event_numb_generator():
    events = TgEvent.objects.all()
    base_numb = 1
    for num in events:
        numb = num.event_number
        int_numb = numb.split('-')
        if int(int_numb[1]) > base_numb:
            base_numb = int(int_numb[1])
    base_numb = base_numb + 1
    next_numb = 'БР-000' + str(base_numb)
    return next_numb
