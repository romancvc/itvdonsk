from postgres_req import event_numb_generator

ERROR_RECOGNISE = "Извините, я вас не понял. Попробуйте еще раз."

text_cmd_start = f'<b><i>Добро пожаловать! Вас приветствует телеграм-бот компании "Бизнес решения"</i></b> \n\n' \
                 f'Мы являемся официальным партнером фирмы 1С и предоставляем широкий спектр услуг ' \
                 f'по автоматизации бизеса:\n' \
                 f'✅продаём программы 1С\n' \
                 f'✅дорабатываем их под ваши нужды\n' \
                 f'✅настраиваем учет\n' \
                 f'✅и многое другое!\n\n' \
                 f'Для продолжения нажмите кнопку внизу 👇🏻️'

text_cmd_start_with_authorization = f'С возвращением!\n\n' \
                                    'Чтобы оставить заявку, просто \n<i><b>🎙запишите ' \
                                    'голосовое сообщение с вашей проблемой🎙</b></i> и ' \
                                    'вам перезвонит первый освободившийся' \
                                    ' специалист.\n\n'

text_process_without_authorization1 = '❗️Без авторизации функционал ограничен❗️'
text_process_without_authorization2 = 'Если у вас возникли проблемы с программой 1С ' \
                                      'или вы хотите проконсультироваться со специалистом' \
                                      ' - оставьте заявку. Для этого просто \n<i><b>🎙запишите ' \
                                      'голосовое сообщение с вашей проблемой🎙</b></i> и ' \
                                      'вам перезвонит первый освободившийся' \
                                      ' специалист.\n\n'
text_process_without_authorization3 = 'Если хотите, чтобы ваши заявки были в приоритете, необходимо авторизоваться. ' \
                                      'Для этого нажмите кнопку внизу 👇🏻'

text_suport = 'Чтобы оставить заявку, просто \n<i><b>🎙запишите ' \
              'голосовое сообщение с вашей проблемой🎙</b></i> и ' \
              'вам перезвонит первый освободившийся' \
              ' специалист.'

text_process_authorization = 'Для авторизации, отправьте полученный от менеджера пароль.\n' \
                             'Чтобы получить пароль - позвоните нам по телефону ниже 👇🏻'

text_with_authorization = 'Если у вас возникли проблемы с программой 1С ' \
                          'или вы хотите проконсультироваться со специалистом' \
                          ' - оставьте заявку. Для этого просто \n<i><b>🎙запишите ' \
                          'голосовое сообщение с вашей проблемой🎙</b></i> и ' \
                          'вам перезвонит первый освободившийся' \
                          ' специалист.\n\n'

bot_text = f"Ваша заявка создана. В ближайшее время с вами свяжется специалист."

after_submit = f'Для борьбы со спамом мы установили ограничение на заявки. ' \
               f'Новую заявку вы сможете оставить не ранее, чем через час.\n\n' \
               f'Для выхода в главное меню введите или нажмите 👉🏻 /start'
