from aiogram import Bot, Dispatcher, executor, types
from keyboards import ikb, kb, kbsuper, ikbuilding, ikbsuper, ikbadd, ikbchange
from config import TOKEN_API #из файла config импортируем токен бота
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from auth import import_bd, check_user_bd, check_audience, delete_audience, add_audience, change_seats_audience, change_computer_audience, change_projector_audience, change_sockets_audience
from const import building_data, building_number, registration_username, registration_password,entrance_username,entrance_password, room_number, access, all_info, cntseats, cntcomputer, cntprojector, cntsockets
import re

import os
import speech_recognition as sr
import soundfile as sf




class RegistrationStates(StatesGroup): # Обработчики для регистрации
    WAITING_FOR_USERNAME = State()
    WAITING_FOR_PASSWORD = State()

class EntranceStates(StatesGroup): # Обработчики для входа
    WAITING_FOR_USERNAME = State()
    WAITING_FOR_PASSWORD = State()

class AudienceForm(StatesGroup): # Обработчик для про-аудиторий
    waiting_for_building = State()
    waiting_for_room = State()

class DeleteAudienceForm(StatesGroup): # Обработчик для удаления аудиторий
    waiting_for_delete_building = State()
    waiting_for_delete_room = State()

class AddAudienceForm(StatesGroup): # Обработчик для добавления аудиторий
    waiting_for_add_building = State()

class AddAudienceVoiceForm(StatesGroup):
    waiting_for_add_voice_building = State()

class ChangeAudienceForm(StatesGroup): # Обработчик для изменения аудиторий
    waiting_for_change_building = State()
    waiting_for_change_room = State()

class ChangeSeatsAudienceForm(StatesGroup): # Обработчик для изменения аудиторий
    waiting_for_change_seats_building = State()

class ChangeComputerAudienceForm(StatesGroup): # Обработчик для изменения аудиторий
    waiting_for_change_computer_building = State()

class ChangeProjectorAudienceForm(StatesGroup): # Обработчик для изменения аудиторий
    waiting_for_change_projector_building = State()

class ChangeSocketsAudienceForm(StatesGroup): # Обработчик для изменения аудиторий
    waiting_for_change_sockets_building = State()


bot = Bot(token=TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Я запустился')


# Передаем параметр reply_markup=kb для создания кнопки (только для команды start)
@dp.message_handler(commands=['start']) # обрабатываем команду start
async def start_command(message: types.Message):
    await message.answer(text='Добро пожаловать в DSTU_audience! Наш бот позволяет вносить данные об аудиториях ДГТУ, с помощью голосовых сообщений. '
                              ' \n <b>Выберите, что хотите сделать:</b>', parse_mode='HTML', reply_markup=ikb)
    await message.delete()


@dp.message_handler(commands=['info_building']) # обрабатываем команду info_building
async def info_building_command(message: types.Message):
    await message.answer(text='Наш вуз имеет 15 учебных корпусов '
                              ' \n <b>Выберите, геолокацию какого ты хочешь узнать:</b>', parse_mode='HTML', reply_markup=ikbuilding)
    await message.delete()

@dp.message_handler(commands=['info_dgtu']) # обрабатываем команду info_dgtu
async def info_dgtu_command(message: types.Message):
    await message.answer(text='Донской государственный технический университет (ДГТУ) – крупнейший на Юге России, '
                              'динамично развивающийся научно-образовательный комплекс. Вуз реализует систему непрерывного'
                              ' образования, объединившую концепцию раннего творческого развития личности и практическую'
                              ' профессиональную подготовку выпускника. Университет вовлекает в образовательный процесс'
                              ' пятилетнего ребенка и выпускает профессионала, готового сразу по получении диплома'
                              ' включиться в производственный процесс. ')
    await message.delete()

@dp.message_handler(commands=['audience'])
async def audience_command(message: types.Message):
    await message.answer(
        text='Здесь вы можете узнать информацию о наличии оборудования в аудитории.'
             ' \nПожалуйста, выберите корпус:', parse_mode='HTML')

    await message.delete()
    await AudienceForm.waiting_for_building.set()

@dp.message_handler(commands=['pro_audience']) # обрабатываем команду start
async def pro_audience_command(message: types.Message):
    await message.answer(text='Здесь вы можете узнать, добавить, удалить информацию о наличии оборудования в аудитории. '
                              ' \n <b>Выберите, что хотите сделать:</b>', parse_mode='HTML', reply_markup=ikbsuper)
    await message.delete()


@dp.callback_query_handler()
async def callback_authentication(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'registration':  # колбек для регистрации
        await callback.message.answer('Введите логин')
        await RegistrationStates.WAITING_FOR_USERNAME.set()

    elif callback.data=='entrance':  # колбек для входа
        await callback.message.answer('Введите логин')
        await EntranceStates.WAITING_FOR_USERNAME.set()

    data = building_data.get(callback.data)
    if data:

        await bot.send_venue(callback.from_user.id, data['latitude'], data['longitude'], data['title'], data['address'])

    elif callback.data=='look':
        await callback.message.answer("Введите номер корпуса")
        await AudienceForm.waiting_for_building.set()
    elif callback.data=='delete':
        await callback.message.answer("Введите номер корпуса")
        await DeleteAudienceForm.waiting_for_delete_building.set()
    elif callback.data=='add':
        await callback.message.answer("Выберите вариант ввода информации:", reply_markup=ikbadd)
    elif callback.data=='addword':
        await callback.message.answer("Пожалуйста, введите данные в следующем порядке \n(целые числа): \n"
                                      "Номер корпуса: \n"
                                      "Номер аудитории: \n"
                                      "Количество мест: \n"
                                      "Количество компьютеров: \n"
                                      "Количество проекторов: \n"
                                      "Количество розеток: ")
        await AddAudienceForm.waiting_for_add_building.set()

    elif callback.data=="change":
        await callback.message.answer("Введите номер корпуса")
        await ChangeAudienceForm.waiting_for_change_building.set()
    elif callback.data=="cntseats":
        await callback.message.answer("Введите новое значение")
        await ChangeSeatsAudienceForm.waiting_for_change_seats_building.set()
    elif callback.data=="cntcomputer":
        await callback.message.answer("Введите новое значение")
        await ChangeComputerAudienceForm.waiting_for_change_computer_building.set()
    elif callback.data == "cntprojector":
        await callback.message.answer("Введите новое значение")
        await ChangeProjectorAudienceForm.waiting_for_change_projector_building.set()
    elif callback.data == "cntsockets":
        await callback.message.answer("Введите новое значение")
        await ChangeSocketsAudienceForm.waiting_for_change_sockets_building.set()
    elif callback.data=='addvoice':
        await callback.message.answer("Пожалуйста, введите данные в следующем порядке \n(целые числа): \n"
                                      "Номер корпуса: \n"
                                      "Номер аудитории: \n"
                                      "Количество мест: \n"
                                      "Количество компьютеров: \n"
                                      "Количество проекторов: \n"
                                      "Количество розеток: \n"
                                      "Выдержите время после начала записи голосового сообщения перед тем, как начнете говорить ")
        await AddAudienceVoiceForm.waiting_for_add_voice_building.set()


@dp.message_handler(content_types=types.ContentType.VOICE, state=AddAudienceVoiceForm.waiting_for_add_voice_building)
async def process_voice_message(message: types.Message, state: FSMContext):
    if message.voice:
        # Получаем объект File из сообщения пользователя
        voice_file = await bot.get_file(message.voice.file_id)
        voice_path = voice_file.file_path
        # Генерируем путь для сохранения файла
        file_name = f'{message.voice.file_id}.ogg'
        file_path = os.path.join('C:\\Users\\ASUS\\DSTU_audience\\project', file_name)
        # Скачиваем голосовое сообщение
        await bot.download_file(voice_path, file_path)
        # Конвертируем аудиофайл в формат WAV
        ogg_file_path = f'{message.voice.file_id}.ogg'
        wav_file_path = os.path.join('C:\\Users\\ASUS\\DSTU_audience\\project', ogg_file_path)
        # Чтение аудиофайла в формате OGG
        audio_data, sample_rate = sf.read(ogg_file_path)
        # Запись аудиофайла в формате WAV
        sf.write(wav_file_path, audio_data, sample_rate, format='WAV')
        # Распознаём речь из аудиофайла
        r = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='ru')  # Можно указать другой язык, если необходимо
        print(text)
# Добавляем аудиторию в бд
        global all_info
        all_info = text
        info_from_bd = re.findall(r'\d+', all_info)
        print(info_from_bd)
        if len(info_from_bd) == 6:
            building = (info_from_bd[0])
            room = (info_from_bd[1])
            seats = (info_from_bd[2])
            computer = (info_from_bd[3])
            projector = (info_from_bd[4])
            sockets = (info_from_bd[5])

            add_audience(building, room, seats, computer, projector, sockets)
            await message.answer(f'Внесена новая аудитория {building}-{room}')
            await state.finish()
        else:
            await message.answer("Перезапишите ввод, нажав на кнопку Голосовой ввод")

    else:
        # Если сообщение не содержит голосового, отправляем пользователю сообщение об ошибке
        await message.reply("Что-то пошло не так, повторите ввод")
    await state.finish()



@dp.message_handler(state=ChangeSeatsAudienceForm.waiting_for_change_seats_building)
async def process_change_seats_building(message: types.Message, state: FSMContext):
    global building_number
    global room_number
    global cntseats
    cntseats = message.text
    change_seats_audience(building_number, room_number, cntseats )
    await message.answer("Данные изменены")
    audience = check_audience(building_number, room_number)
    if audience:
        building = audience[0]
        room = audience[1]
        seats = audience[2]
        computer = audience[3]
        projector = audience[4]
        sockets = audience[5]
        await message.answer(f"Номер корпуса: {building}\n"
                             f"Номер аудитории: {room}\n"
                             f"Количество мест: {seats}\n"
                             f"Количество компьютеров: {computer}\n"
                             f"Количество проекторов: {projector}\n"
                             f"Количество розеток: {sockets}")

    await state.finish()


@dp.message_handler(state=ChangeComputerAudienceForm.waiting_for_change_computer_building)
async def process_change_computer_building(message: types.Message, state: FSMContext):
    global building_number
    global room_number
    global cntcomputer
    cntcomputer = message.text
    change_computer_audience(building_number, room_number, cntcomputer )
    await message.answer("Данные изменены")
    audience = check_audience(building_number, room_number)
    if audience:
        building = audience[0]
        room = audience[1]
        seats = audience[2]
        computer = audience[3]
        projector = audience[4]
        sockets = audience[5]
        await message.answer(f"Номер корпуса: {building}\n"
                             f"Номер аудитории: {room}\n"
                             f"Количество мест: {seats}\n"
                             f"Количество компьютеров: {computer}\n"
                             f"Количество проекторов: {projector}\n"
                             f"Количество розеток: {sockets}")

    await state.finish()


@dp.message_handler(state=ChangeProjectorAudienceForm.waiting_for_change_projector_building)
async def process_change_projector_building(message: types.Message, state: FSMContext):
    global building_number
    global room_number
    global cntprojector
    cntprojector = message.text
    change_projector_audience(building_number, room_number, cntprojector )
    await message.answer("Данные изменены")
    audience = check_audience(building_number, room_number)
    if audience:
        building = audience[0]
        room = audience[1]
        seats = audience[2]
        computer = audience[3]
        projector = audience[4]
        sockets = audience[5]
        await message.answer(f"Номер корпуса: {building}\n"
                             f"Номер аудитории: {room}\n"
                             f"Количество мест: {seats}\n"
                             f"Количество компьютеров: {computer}\n"
                             f"Количество проекторов: {projector}\n"
                             f"Количество розеток: {sockets}")

    await state.finish()


@dp.message_handler(state=ChangeSocketsAudienceForm.waiting_for_change_sockets_building)
async def process_change_sockets_building(message: types.Message, state: FSMContext):
    global building_number
    global room_number
    global cntsockets
    cntsockets = message.text
    change_sockets_audience(building_number, room_number, cntsockets )
    await message.answer("Данные изменены")
    audience = check_audience(building_number, room_number)
    if audience:
        building = audience[0]
        room = audience[1]
        seats = audience[2]
        computer = audience[3]
        projector = audience[4]
        sockets = audience[5]
        await message.answer(f"Номер корпуса: {building}\n"
                             f"Номер аудитории: {room}\n"
                             f"Количество мест: {seats}\n"
                             f"Количество компьютеров: {computer}\n"
                             f"Количество проекторов: {projector}\n"
                             f"Количество розеток: {sockets}")

    await state.finish()

# Обработчик для изменения оборудования
@dp.message_handler(state=ChangeAudienceForm.waiting_for_change_building)
async def process_change_building(message: types.Message, state: FSMContext):
    global building_number
    building_number = message.text
    await message.answer('Пожалуйста, введите номер аудитории:')
    await ChangeAudienceForm.waiting_for_change_room.set()


# Принимаем номер аудитории
@dp.message_handler(state=ChangeAudienceForm.waiting_for_change_room)
async def process_change_room(message: types.Message, state: FSMContext):
    global room_number
    room_number = message.text
    audience = check_audience(building_number, room_number)
    if audience:
        building = audience[0]
        room = audience[1]
        seats = audience[2]
        computer = audience[3]
        projector = audience[4]
        sockets = audience[5]
        await message.answer(f"Номер корпуса: {building}\n"
                             f"Номер аудитории: {room}\n"
                             f"Количество мест: {seats}\n"
                             f"Количество компьютеров: {computer}\n"
                             f"Количество проекторов: {projector}\n"
                             f"Количество розеток: {sockets}")
        await message.answer("Что вы хотите изменить?", reply_markup=ikbchange)
    else:
        await message.answer("Аудитория не найдена")

    await state.finish()
# Обработчик для вывода информации о аудитории pro

# Принимаем номер корпуса
@dp.message_handler(state=AudienceForm.waiting_for_building)
async def process_building(message: types.Message, state: FSMContext):
    global building_number
    building_number = message.text
    await message.answer('Пожалуйста, введите номер аудитории:')
    await AudienceForm.waiting_for_room.set()


# Принимаем номер аудитории
@dp.message_handler(state=AudienceForm.waiting_for_room)
async def process_room(message: types.Message, state: FSMContext):
    room_number = message.text
    audience = check_audience(building_number, room_number)
    if audience:
        building = audience[0]
        room = audience[1]
        seats = audience[2]
        computer = audience[3]
        projector = audience[4]
        sockets = audience[5]
        await message.answer(f"Номер корпуса: {building}\n"
                             f"Номер аудитории: {room}\n"
                             f"Количество мест: {seats}\n"
                             f"Количество компьютеров: {computer}\n"
                             f"Количество проекторов: {projector}\n"
                             f"Количество розеток: {sockets}")
    else:
        await message.answer("Аудитория не найдена")

    await state.finish()


# Обработчик принимающий номер корпуса для удаления
@dp.message_handler(state=DeleteAudienceForm.waiting_for_delete_building)
async def process_delete_building(message: types.Message, state: FSMContext):
    global building_number
    building_number = message.text
    await message.answer('Пожалуйста, введите номер аудитории:')
    await DeleteAudienceForm.waiting_for_delete_room.set()


# Обработчик принимающий номер аудитории для удаления
@dp.message_handler(state=DeleteAudienceForm.waiting_for_delete_room)
async def process_delete_room(message: types.Message, state: FSMContext):
    global room_number
    room_number = message.text
    audience = check_audience(building_number, room_number)
    if audience:
        delete_audience(building_number, room_number)
        await message.answer("Аудитория удалена")
    else:
        await message.answer("Аудитория не найдена")
    await state.finish()


# Обработчик для внесения новой аудитории с оборудованием
@dp.message_handler(state=AddAudienceForm.waiting_for_add_building)
async def process_add_building(message: types.Message, state: FSMContext):
    global all_info
    all_info = message.text
    info_from_bd = re.findall(r'\d+', all_info)

    building = (info_from_bd[0])
    room = (info_from_bd[1])
    seats=(info_from_bd[2])
    computer=(info_from_bd[3])
    projector=(info_from_bd[4])
    sockets=(info_from_bd[5])

    add_audience(building, room, seats, computer, projector, sockets)
    await message.answer(f'Внесена новая аудитория {building}-{room}')
    await state.finish()


# Обработчик логина при регистрации
@dp.message_handler(state=RegistrationStates.WAITING_FOR_USERNAME)
async def registration_username(message: types.Message):
    global registration_username
    registration_username = message.text
    await message.answer('Введите пароль')
    await RegistrationStates.WAITING_FOR_PASSWORD.set()

# Обработчик пароля при регистрации
@dp.message_handler(state=RegistrationStates.WAITING_FOR_PASSWORD)
async def registration_password(message: types.Message, state: FSMContext):
    global registration_password
    registration_password = message.text
    await state.finish()
    await message.answer('Спасибо за регистрацию!', reply_markup=kb)
    import_bd(registration_username, registration_password)

# Обработчик логина при входе
@dp.message_handler(state=EntranceStates.WAITING_FOR_USERNAME)
async def entrance_username(message: types.Message):
    global entrance_username
    entrance_username = message.text
    await message.answer('Введите пароль')
    await EntranceStates.WAITING_FOR_PASSWORD.set()

# Обработчик пароля при входе
@dp.message_handler(state=EntranceStates.WAITING_FOR_PASSWORD)
async def entrance_password(message: types.Message, state: FSMContext):
    global entrance_password
    entrance_password = message.text

    access_level = check_user_bd(entrance_username, entrance_password)

    if access_level == "kbsuper":
        await message.answer(f"Здравствуйте, {entrance_username}!", reply_markup=kbsuper)
    elif access_level == "kb":
        await message.answer(f"Здравствуйте, {entrance_username}!", reply_markup=kb)
    else:
        await message.answer("Такого аккаунта не существует")

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

