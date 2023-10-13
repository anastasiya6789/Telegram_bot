from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove



kb=ReplyKeyboardMarkup(resize_keyboard=True) # параметр one_time_keyboard=False чтобы клавиатура не пропадала
b1=KeyboardButton('/info_dgtu')
b2=KeyboardButton('/audience')
b3=KeyboardButton('/info_building')
kb.add(b1, b2).add(b3)

ikbuilding=InlineKeyboardMarkup(row_width=4)
ibb1=InlineKeyboardButton('1',
                         callback_data='1')
ibb2=InlineKeyboardButton('2',
                         callback_data='2')
ibb3=InlineKeyboardButton('6',
                         callback_data='6')
ibb4=InlineKeyboardButton('7',
                         callback_data='7')
ibb5=InlineKeyboardButton('8',
                         callback_data='8')
ibb6=InlineKeyboardButton('10',
                         callback_data='10')
ibb7=InlineKeyboardButton('11',
                         callback_data='11')
ibb8=InlineKeyboardButton('21',
                         callback_data='21')
ibb9=InlineKeyboardButton('22',
                         callback_data='22')
ibb10=InlineKeyboardButton('24',
                         callback_data='24')
ibb11=InlineKeyboardButton('25',
                         callback_data='25')
ibb12=InlineKeyboardButton('26',
                         callback_data='26')
ibb13=InlineKeyboardButton('3, 4, 5',
                         callback_data='345')

ikbuilding.add(ibb13).add(ibb1,ibb2,ibb3,ibb4).add(ibb5,ibb6,ibb7,ibb8).add(ibb9,ibb10,ibb11,ibb12)


kbsuper=ReplyKeyboardMarkup(resize_keyboard=True)
bp1=KeyboardButton('/info_building')
bp2=KeyboardButton('/pro_audience')
kbsuper.add(bp1, bp2)

ikb=InlineKeyboardMarkup(row_width=2)
ib1=InlineKeyboardButton('Регистрация',
                         callback_data='registration')
ib2=InlineKeyboardButton('Вход',
                         callback_data='entrance')

ikb.add(ib1,ib2)


#клавиатура, для редактирования аудиторий
ikbsuper=InlineKeyboardMarkup(row_width=1)
ibs1=InlineKeyboardButton('Добавить аудиторию',
                         callback_data='add')
ibs2=InlineKeyboardButton('Изменить данные',
                         callback_data='change')
ibs3=InlineKeyboardButton('Удалить аудиторию',
                         callback_data='delete')
ibs4=InlineKeyboardButton('Просмотреть оборудование',
                         callback_data='look')

ikbsuper.add(ibs1).add(ibs2).add(ibs3).add(ibs4)



ikbadd=InlineKeyboardMarkup(row_width=2)
iba1=InlineKeyboardButton('Голосовой ввод',
                         callback_data='addvoice')
iba2=InlineKeyboardButton('Текстовый ввод',
                         callback_data='addword')

ikbadd.add(iba1,iba2)


ikbchange=InlineKeyboardMarkup(row_width=1)
ibc1=InlineKeyboardButton('Количество мест',
                         callback_data='cntseats')
ibc2=InlineKeyboardButton('Количество компьютеров',
                         callback_data='cntcomputer')
ibc3=InlineKeyboardButton('Количество проекторов',
                         callback_data='cntprojector')
ibc4=InlineKeyboardButton('Количество розеток',
                         callback_data='cntsockets')

ikbchange.add(ibc1).add(ibc2).add(ibc3).add(ibc4)

