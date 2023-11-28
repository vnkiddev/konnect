from django.db import connection


def qr_detail(qr_code):
    cmd = "SELECT name FROM tb_name WHERE qtype IN (SELECT qtype FROM qr WHERE qrid = '"+qr_code+"');"
    with connection.cursor() as cursor:
        cursor.execute(cmd)
        print(cmd)
        row = cursor.fetchone()
        if row == None:
            return [{"key":"QRID","value":"Mã QR với sản phẩm này chưa tồn tại"}]
        else:
            table_name = row[0]
            cmd = 'SELECT * FROM '+table_name+" where qrid ='" +qr_code+ "';"
            cursor.execute(cmd)
            values = cursor.fetchone()
            cmd = 'SELECT * FROM '+table_name+' limit 1'
            cursor.execute(cmd)
            keys = cursor.fetchone()
            result = []

            for i in range(len(keys)):
                result.append({'key':keys[i],'value':values[i]})
            return result

def drop_table(table_name):
    cmd = 'DROP TABLE '+table_name
    try:
        with connection.cursor() as cursor:
            cursor.execute(cmd)
            connection.commit()
            return True
    except Exception as e:
        print(e)
        return False

def migrate_table(sheet_values,table_name, header_as_collumn = False):
    drop_table(table_name)
    cmd = 'CREATE TABLE '+table_name +'('
    if not header_as_collumn: #insert header
        header = ['qrid']
        for i in range(1, len(sheet_values[0])):
            header.append('collumn_' + str(i))
        sheet_values.insert(0,header)
    for i in sheet_values[0]:
        cmd = cmd + i + ' text,'
    cmd = cmd[:-1]+ ');'
    print('create:',cmd)
    with connection.cursor() as cursor:
        cursor.execute(cmd)
        connection.commit()
    cmd = "INSERT INTO " + table_name + '('
    for i in sheet_values[0]:
        cmd = cmd + i + ','
    cmd = cmd[:-1] + ') VALUES '
    for row in sheet_values[1:]:
        cmd = cmd + array_to_insert(row)
    cmd = cmd[:-1] + ';'
    print('Insert', cmd)
    with connection.cursor() as cursor:
        cursor.execute(cmd)
        connection.commit()
    return True

def array_to_insert(array):
    sql = '('
    for e in array:
        sql = sql + "'" + e + "',"
    return sql[:-1] + '),'