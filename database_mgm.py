import json
import sqlite3
import time
from datetime import date, timedelta

DATABASE = 'pedidos.db'

# DEFINES
INFO_NO_MATERIAL = 6
OK = 1

INPUT_ID = 'input-id'
INPUT_OBRA = 'input-obra'
INPUT_PROVEEDOR = 'input-proveedor'
INPUT_ENTREGA = 'input-entrega'
INPUT_FECHA_ENTREGA = 'input-fecha-entrega'
INPUT_FECHA_PEDIDO = 'input-fechapedido'
INPUT_ESTADO_PEDIDO = 'input-estadopedido'
INPUT_ESTADO_ENTREGA = 'input-estadoentrega'
INPUT_FECHA_ENTREGA2 = 'input-fechaentrega'
INPUT_MATERIALES1 = 'input-material-add'
INPUT_FECHA_COMPRA = 'input-fechacompra'
INPUT_COMENTARIO = 'input-comentario'
INPUT_COMPRA = 'input-compra'
NO_SELECTED = 'No seleccionado'


def parse_json_data(json_data):
    counter = 0
    lista_info = []
    lista_materiales = []
    loaded = json.loads(json_data)

    # First check if there is any empty place
    if loaded[INPUT_OBRA] == [''] or loaded[INPUT_MATERIALES1] == ['']:
        return None, None

    # Put everything in a list until materials
    for inputs in loaded:
        if counter < 2:
            # print(loaded[inputs][0])
            lista_info.append(loaded[inputs][0])
        else:
            lista_materiales.append(loaded[inputs][0])
        counter = counter + 1

    return lista_info, lista_materiales


def push_database(info, materials):

    # Dia y hora actual
    named_tuple = time.localtime()
    time_string = time.strftime("%d-%m-%Y", named_tuple)

    conn = sqlite3.connect(DATABASE)
    newlist = []
    counter = 1

    try:
        c = conn.cursor()

        # Information list to tuple
        info.insert(1, time_string)
        params = tuple(info)
        # print(params)

        # Execute and returns rowId
        row = c.execute(
            '''INSERT INTO pedidos VALUES (NULL,?,?,'Pendiente',NULL,'Pendiente',NULL,?)''', params).lastrowid
        idpedidos = int(row)
        
        # Materials list to tuple
        for row in materials:
            newlist.append(counter)
            for i in row:
                newlist.append(i)
            newlist.append(idpedidos)
            
            params = tuple(newlist)
            c.execute('''INSERT INTO materiales VALUES (?,?,?,?,NULL,?)''', params)
            newlist.clear()
            counter = counter + 1

        conn.commit()

    except Exception as err:
        print("Can't insert values to pedidos and materiales")
        print(err)

    finally:
        if conn:
            print("Close connection")
            conn.close()


def create_tables(database):
    try:
        print("Creating tables if not exists")
        conn = sqlite3.connect(str(database))
        c = conn.cursor()

        # Create tables on database
        c.execute('''CREATE TABLE IF NOT EXISTS pedidos (
	                    id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	                    Obra	TEXT,
	                    Fecha_pedido	TEXT,
	                    Estado_pedido	TEXT,
	                    Fecha_compra	TEXT,
                        Estado_entrega	TEXT,
                        Fecha_entrega   TEXT,
                        Comentario      TEXT
                        )''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS materiales (idmat INTEGER, Material TEXT, Cantidad INTEGER, Unidad TEXT,Proveedor TEXT, idpedido INTEGER) ''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS proveedores (idprov INTEGER NOT NULL PRIMARY KEY, Nombre TEXT)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS Obras (idobra INTEGER NOT NULL PRIMARY KEY, Obra TEXT)''')

        # Commit and close database
        conn.commit()
        conn.close()
    except:
        print("Can't create tables")
        return False


def get_all_data(flag=False):
    conn = sqlite3.connect(DATABASE)
    datalist = []

    try:
        if flag == True:
            c = conn.cursor()
            c.execute('''SELECT * FROM pedidos ORDER BY id DESC LIMIT 11''')
        else:
            c = conn.cursor()
            c.execute('''SELECT * FROM pedidos''')

        for row in c:
            datalist.append(list(row))

        for row in datalist:
            for idx, data in enumerate(row):
                if data == None:
                    row[idx] = 'None'

        return datalist

    except Exception as err:
        print("Error gettinga data")
        print(err)
    finally:
        if conn:
            conn.close()


def delete_from_database(json_data):
    loaded = json.loads(json_data)
    valor = 0

    # First check if there is any empty place
    for inputs in loaded:
        # print(loaded[inputs])
        if loaded[inputs] == ['']:
            return False

    for inpus in loaded:
        valor = loaded[inputs]

    params = (str(valor[0]),)

    conn = sqlite3.connect(DATABASE)
    try:
        c = conn.cursor()
        c.execute('''DELETE FROM pedidos WHERE id=?''', params)
        c.execute('''DELETE FROM materiales WHERE idpedidos=?''', params)
        conn.commit()

    except Exception as err:
        print(err)
        return False

    finally:
        if conn:
            c.close()
            conn.close()

    return True


def filter_from_database(inputid, json_data):
    loaded = json.loads(json_data)
    filtersize = len(loaded)
    filterlist = []
    materialist = []

    conn = sqlite3.connect(DATABASE)
    try:
        c = conn.cursor()

        # Check if there is any empty
        if inputid != 0 or loaded[INPUT_OBRA] != [''] or loaded[INPUT_PROVEEDOR] != ['']:

            if inputid != 0 and loaded[INPUT_OBRA] != [''] and loaded[INPUT_PROVEEDOR] != ['']:
                params = (inputid, loaded[INPUT_OBRA]
                          [0], loaded[INPUT_PROVEEDOR][0])
                c.execute(
                    '''SELECT * FROM pedidos WHERE id=? AND Obra=? AND Proveedor=?''', params)
                for row in c:
                    filterlist.append(list(row))
                c.execute(
                    '''SELECT * FROM materiales WHERE idpedidos=?''', (inputid,))
                materialist.clear()
                for row in c:
                    row = row[0:3]
                    materialist.append(list(row))

            elif inputid != 0 and loaded[INPUT_OBRA] != ['']:
                params = (inputid, loaded[INPUT_OBRA][0])
                c.execute(
                    '''SELECT * FROM pedidos WHERE id=? AND Obra=?''', params)
                for row in c:
                    filterlist.append(list(row))
                c.execute(
                    '''SELECT * FROM materiales WHERE idpedidos=?''', (inputid,))
                materialist.clear()
                for row in c:
                    row = row[0:3]
                    materialist.append(list(row))

            elif inputid != 0 and loaded[INPUT_PROVEEDOR] != ['']:
                params = (inputid, loaded[INPUT_PROVEEDOR][0])
                c.execute(
                    '''SELECT * FROM pedidos WHERE id=? AND Proveedor=?''', params)
                for row in c:
                    filterlist.append(list(row))
                c.execute(
                    '''SELECT * FROM materiales WHERE idpedidos=?''', (inputid,))
                materialist.clear()
                for row in c:
                    row = row[0:3]
                    materialist.append(list(row))

            elif loaded[INPUT_OBRA] != [''] and loaded[INPUT_PROVEEDOR] != ['']:
                params = (loaded[INPUT_OBRA][0], loaded[INPUT_PROVEEDOR][0])
                c.execute(
                    '''SELECT * FROM pedidos WHERE Obra=? AND Proveedor=?''', params)
                for row in c:
                    filterlist.append(list(row))

            elif inputid != 0:
                params = (inputid,)
                c.execute('''SELECT * FROM pedidos WHERE id=?''', params)
                for row in c:
                    filterlist.append(list(row))
                c.execute(
                    '''SELECT * FROM materiales WHERE idpedidos=?''', (inputid,))
                materialist.clear()
                for row in c:
                    row = row[0:3]
                    materialist.append(list(row))

            elif loaded[INPUT_OBRA] != ['']:
                params = (loaded[INPUT_OBRA][0],)
                c.execute('''SELECT * FROM pedidos WHERE Obra=?''', params)
                for row in c:
                    filterlist.append(list(row))

            elif loaded[INPUT_PROVEEDOR] != ['']:
                params = (loaded[INPUT_PROVEEDOR][0],)
                c.execute('''SELECT * FROM pedidos WHERE Proveedor=?''', params)
                for row in c:
                    filterlist.append(list(row))

            conn.commit()

            for row in filterlist:
                for idx, data in enumerate(row):
                    if data == None:
                        row[idx] = 'None'

            for row in materialist:
                for idx, data in enumerate(row):
                    if data == None:
                        row[idx] = 'None'

            if conn:
                conn.close()

            return filterlist, materialist

        else:
            if conn:
                conn.close()
            return False, False

    except Exception as err:
        print(err)
        return False, False


def filter_data_by(option, json_data):
    loaded = json.loads(json_data)
    filterlist = []
    materialist = []
    idlist = []

    if option == "id" and loaded[INPUT_ID] == ['']:
        return False,False
    elif option == "obra" and loaded[INPUT_OBRA] == ['']:
        return False,False
    elif option == "proveedor" and loaded[INPUT_PROVEEDOR] == ['']:
        return False,False

    conn = sqlite3.connect(DATABASE)
    try:
        c = conn.cursor()

        if option == "id":
            params = (loaded[INPUT_ID][0],)
            c.execute('''SELECT * FROM pedidos WHERE id=?''', params)
            for row in c:
                filterlist.append(list(row))
            c.execute('''SELECT * FROM materiales WHERE idpedidos=?''', params)
            materialist.clear()
            for row in c:
                row = row[0:5]
                materialist.append(list(row))
        
        elif option == "obra":
            params = (loaded[INPUT_OBRA][0],)
            c.execute('''SELECT * FROM pedidos WHERE Obra=?''', params)
            for row in c:
                filterlist.append(list(row))
        
        elif option == "proveedor":
            params = (loaded[INPUT_PROVEEDOR][0],)
            c.execute('''SELECT idpedidos FROM materiales WHERE Proveedor=?''', params)

            lastrow = 0

            for row in c:
                if lastrow != row:
                    idlist.append(row[0])
                lastrow = row

            for row in idlist:
                params = (row,)
                c.execute('''SELECT * FROM pedidos WHERE id=?''',params)
                for row in c:
                    filterlist.append(list(row))
        
        else:
            if conn:
                conn.close()
            return False, False

        for row in filterlist:
            for idx, data in enumerate(row):
                if data == None:
                    row[idx] = 'None'

        for row in materialist:
            for idx, data in enumerate(row):
                if data == None:
                    row[idx] = 'None'
        
        conn.commit()

        if conn:
            conn.close()

        return filterlist, materialist

    except Exception as err:
        print(err)
        return False, False


def update_database(json_data):
    loaded = json.loads(json_data)

    # First check if ID is not empty
    if loaded[INPUT_ID] == ['']:
        return False

    conn = sqlite3.connect(DATABASE)

    try:
        c = conn.cursor()

        if loaded[INPUT_COMPRA] != ['']:

            if loaded[INPUT_ENTREGA] != ['']:
                params = (loaded[INPUT_ENTREGA][0], loaded[INPUT_ID][0])
                c.execute('''UPDATE pedidos SET Estado_entrega=? WHERE id=?''', params)

            if loaded[INPUT_FECHA_ENTREGA] != ['']:
                params = (loaded[INPUT_FECHA_ENTREGA][0], loaded[INPUT_ID][0])
                c.execute('''UPDATE pedidos SET Fecha_entrega=? WHERE id=?''', params)

            if loaded[INPUT_FECHA_COMPRA] != ['']:
                params = (loaded[INPUT_FECHA_COMPRA][0], loaded[INPUT_ID][0])
                c.execute('''UPDATE pedidos SET Fecha_compra=? WHERE id=?''', params)
        else:
            if conn:
                conn.close()
            return False

        conn.commit()
        if conn:
            conn.close()

        return True

    except Exception as err:
        print(err)
        if conn:
            conn.close()
        return False

def update_data_by(option, json_data):

    # Dia y hora actual
    named_tuple = time.localtime()
    time_string = time.strftime("%d-%m-%Y", named_tuple)

    counter = 0

    loaded = json.loads(json_data)

    for key in loaded.items():
        if counter == 0:
            idnum = key[0]
        counter = counter + 1

    idnum = int(idnum)

    conn = sqlite3.connect(DATABASE)

    try:
        c = conn.cursor()

        if option == 'compra':
            if idnum != 0:
                params = (loaded[str(idnum)][0], idnum)
                c.execute('''UPDATE pedidos SET Estado_pedido=? WHERE id=?''', params)
                c.execute('''UPDATE pedidos SET Fecha_compra=? WHERE id=?''',(time_string,idnum))
            else:
                return False
        
        elif option == 'entrega':
            if idnum != 0:
                if loaded[str(idnum)] != [''] and loaded[INPUT_FECHA_ENTREGA] != ['']:
                    params = (loaded[str(idnum)][0], str(idnum))
                    c.execute('''UPDATE pedidos SET Estado_entrega=? WHERE id=?''', params)
                    params = (loaded[INPUT_FECHA_ENTREGA][0], str(idnum))
                    c.execute('''UPDATE pedidos SET Fecha_entrega=? WHERE id=?''',params)
                else:
                    return False
        
        conn.commit()

        if conn:
            conn.close()
        
        return True

    except Exception as err:
        print(err)
        if conn:
            conn.close()
        return False


def get_proveedores():
    conn = sqlite3.connect(DATABASE)
    proveedores = []

    try:
        c = conn.cursor()

        c.execute('''SELECT Nombre FROM proveedores ORDER BY idprov ASC ''')

        conn.commit()

        for row in c:
            proveedores.append(row[0])

        # print(proveedores)

        if conn:
            conn.close()

        return proveedores

    except Exception as err:

        print(err)
        if conn:
            conn.close()
        return False

def get_obras():
    conn = sqlite3.connect(DATABASE)
    obras = []

    try:
        c = conn.cursor()

        c.execute('''SELECT Obra FROM Obras ORDER BY Obra ASC ''')

        conn.commit()

        for row in c:
            obras.append(row[0])

        # print(proveedores)

        if conn:
            conn.close()

        return obras

    except Exception as err:

        print(err)
        if conn:
            conn.close()
        return False


def reference(data_json):
    loaded = json.loads(data_json)
    if INPUT_ID in loaded:
        if loaded[INPUT_ID] != ['']:
            return loaded[INPUT_ID][0]


def update_materials(json_data):
    loaded = json.loads(json_data)
    proveedores = []
    counter = 1
    idnum = 0

    for key in loaded.items():
        idnum = key[0]
        #print(str(idnum))
    
    conn = sqlite3.connect(DATABASE)

    try:
        c = conn.cursor()
        proveedores = loaded[str(idnum)]
        
        for row in proveedores:
            if row != 'No seleccionado':
                params = (row, str(counter), idnum)
                #print(params)
                c.execute('''UPDATE materiales SET Proveedor=? WHERE idmat=? and idpedidos=?''',params)
            counter = counter + 1
        conn.commit()
        conn.close()
        return True,str(idnum)
    
    except Exception as err:

        print(err)
        if conn:
            conn.close()
        return False,str(idnum)

def filter_updated(idnum):
    filterlist = []
    materialist = []
    #print("id number is", idnum)

    conn = sqlite3.connect(DATABASE)
    try:
        c = conn.cursor()

        if idnum != '0':
            params = (idnum,)
            c.execute('''SELECT * FROM pedidos WHERE id=?''', params)
            for row in c:
                filterlist.append(list(row))
            c.execute('''SELECT * FROM materiales WHERE idpedidos=?''', params)
            materialist.clear()
            for row in c:
                row = row[0:5]
                materialist.append(list(row))

        else:
            if conn:
                conn.close()
            return False, False

        for row in filterlist:
            for idx, data in enumerate(row):
                if data == None:
                    row[idx] = 'None'

        for row in materialist:
            for idx, data in enumerate(row):
                if data == None:
                    row[idx] = 'None'
        
        conn.commit()

        if conn:
            conn.close()

        return filterlist, materialist

    except Exception as err:
        print(err)
        return False, False


def take_info_from(data_json):
    loaded = json.loads(data_json)
    info = []

    if loaded[INPUT_OBRA] == ['No seleccionado']:
        return False
    
    info.append(loaded[INPUT_OBRA][0])
    info.append(loaded[INPUT_COMENTARIO][0])

    return info

def take_material_from(data_json):
    loaded = json.loads(data_json)
    materiales = []
    counter = 0

    for i in loaded:
        if counter > 1:
            if loaded[i] == [''] or loaded[i] == ['seleccionar']:
                return False
            materiales.append(loaded[i][0])
        counter = counter + 1

    num = len(materiales)/3
    if num != 0:
        ret = separate_materials(materiales,num)
    else:
        return False

    #List of lists
    return ret

def separate_materials(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def is_toadd(json_data):
    loads = json.loads(json_data)
    if loads['input-button'] == ["Agregar"]:
        return True
    else:
        return False

def add_proveedor(json_data):
    loads = json.loads(json_data)
    conn = sqlite3.connect(DATABASE)
    try:
        c = conn.cursor()
        c.execute("INSERT INTO proveedores VALUES (NULL,?)",(loads['input-proveedor'][0],))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        if conn:
            conn.close()
        return False

def delete_proveedor(json_data):
    loads = json.loads(json_data)
    conn = sqlite3.connect(DATABASE)
    try:
        c = conn.cursor()
        c.execute("DELETE FROM proveedores WHERE Nombre=?",(loads['input-proveedor'][0],))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        if conn:
            conn.close()
        return False

def add_obra(json_data):
    loads = json.loads(json_data)
    conn = sqlite3.connect(DATABASE)
    try:
        c = conn.cursor()
        c.execute("INSERT INTO Obras VALUES (NULL,?)",(loads['input-obra'][0],))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        if conn:
            conn.close()
        return False

def delete_obra(json_data):
    loads = json.loads(json_data)
    conn = sqlite3.connect(DATABASE)
    try:
        c = conn.cursor()
        c.execute("DELETE FROM Obras WHERE Obra=?",(loads['input-obra'][0],))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        if conn:
            conn.close()
        return False

def obras_listed():
    newlist = []
    obras = get_obras()
    obras.pop(0)
    for i in obras:
        newlist.append([i])

    return newlist

def proveedores_listed():
    newlist = []
    proveedores = get_proveedores()
    proveedores.pop(0)
    for i in proveedores:
        newlist.append([i])

    return newlist

    


    