import sqlite3
from const import building_number, room_number
access=0
def import_bd(registration_username, registration_password):
    con = sqlite3.connect('dstu.db')
    cur = con.cursor()
    a = registration_username
    b = registration_password
    c=access
    query1 = f" INSERT INTO registration (login,password,access) VALUES('{a}','{b}','{c}' )"
    cur.execute(query1)
    con.commit()
    cur.close()
    con.close()

def check_user_bd(entrance_username, entrance_password):
    con = sqlite3.connect('dstu.db')
    cur = con.cursor()
    query = f"SELECT * FROM registration WHERE login='{entrance_username}' AND password='{entrance_password}'"
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        if result[2] == 1:  # Проверяем значение столбца access (индекс 2 в кортеже)
            return "kbsuper"  # Возвращаем 'kbsuper', если access равен 1
        else:
            return "kb"  # Возвращаем 'kb', если access равен 0

    return None  # Возвращаем None, если пользователя не существует

def check_audience(building_number, room_number):
    conn = sqlite3.connect('dstu.db')
    cursor = conn.cursor()

    # Выполняем запрос к базе данных
    cursor.execute("SELECT building, room, seats, computer, projector, sockets FROM audience WHERE building=? AND room=?",
                   (building_number, room_number))

    audience = cursor.fetchone()
    conn.close()
    return audience

def delete_audience(building_number, room_number):
    conn = sqlite3.connect('dstu.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM audience WHERE building=? AND room=? ",
                   (building_number, room_number))
    conn.commit()

    cursor.close()
    conn.close()

def add_audience(building, room, seats, computer, projector, sockets):
    conn = sqlite3.connect('dstu.db')
    cursor = conn.cursor()
    q = f" INSERT INTO audience (building, room, seats, computer, projector, sockets) VALUES('{building}','{room}','{seats}','{computer}','{projector}','{sockets}' )"
    cursor.execute(q)
    conn.commit()

    cursor.close()
    conn.close()


def change_seats_audience(building_number, room_number, cntseats):
    conn = sqlite3.connect('dstu.db')
    cursor = conn.cursor()
    sql_query = f"UPDATE audience SET seats = '{cntseats}' WHERE building='{building_number}' AND room='{room_number}'"
    cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()


def change_computer_audience(building_number, room_number, cntcomputer):
    conn = sqlite3.connect('dstu.db')
    cursor = conn.cursor()
    sql_query = f"UPDATE audience SET computer = '{cntcomputer}' WHERE building='{building_number}' AND room='{room_number}'"
    cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()


def change_projector_audience(building_number, room_number, cntprojector):
    conn = sqlite3.connect('dstu.db')
    cursor = conn.cursor()
    sql_query = f"UPDATE audience SET projector = '{cntprojector}' WHERE building='{building_number}' AND room='{room_number}'"
    cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()

def change_sockets_audience(building_number, room_number, cntsockets):
    conn = sqlite3.connect('dstu.db')
    cursor = conn.cursor()
    sql_query = f"UPDATE audience SET sockets = '{cntsockets}' WHERE building='{building_number}' AND room='{room_number}'"
    cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()




