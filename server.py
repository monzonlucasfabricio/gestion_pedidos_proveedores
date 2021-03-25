from flask import Flask,render_template,request,redirect,url_for
from werkzeug.serving import run_simple
import json
from database_mgm import *

option = 0

app = Flask(__name__)


# Slash method that redirect to /main
@app.route('/', methods = ['GET'])
def index():
    if request.method == 'GET':
        return redirect(url_for('cargar'))

@app.route('/cargar', methods = ['GET','POST'])
def cargar():
    if request.method == 'GET':
        obras = get_obras()
        return render_template('cargar.html',obras = obras)
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        data_json = json.dumps(data)

        # Parsing the data and return success or not
        #info,materials = parse_json_data(data_json)

        info = take_info_from(data_json)
        materials = take_material_from(data_json)

        if info == False or materials == False:
            obras = get_obras()
            return render_template('cargar.html', error = 'Faltan completar datos', obras = obras)
            
        push_database(info,materials)

        obras = get_obras()
        return render_template('cargar.html',error = 'El nuevo pedido ha sido guardado', obras = obras)


@app.route('/actualizar', methods = ['GET','POST'])
def actualizar():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('actualizar.html', data = data)
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        if update_database(data_json) == False:
            data = get_all_data()
            return render_template('actualizar.html', error = 'Falta datos', data = data)
        data = get_all_data()
        return render_template('actualizar.html',data = data, error = 'Actualizado')


@app.route('/actualizar-compra-pre', methods = ['GET','POST'])
def actualizar_compra_pre():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('actualizar-compra-pre.html', data = data)
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        loaded = json.loads(data_json)
        if loaded[INPUT_ID] != ['']:
            idnum = loaded[INPUT_ID][0]
        data,materiales = filter_data_by('id',data_json)
        if data == False:
            data = get_all_data()
            return render_template('actualizar-compra-pre.html', data = data, error = 'Faltan datos')
        return render_template('actualizar-compra.html', data = data, error = 'Filtrado OK', materiales = materiales, idnum = idnum)

@app.route('/actualizar-compra', methods = ['GET','POST'])
def actualizar_compra():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('actualizar-compra.html', data = data)
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        print(data_json)
        if update_data_by('compra',data_json) == False:
            data = get_all_data()
            return render_template('actualizar-compra-pre.html', error = 'Falta datos', data = data)

        data = get_all_data()
        return render_template('actualizar-compra-pre.html',data = data, error = 'Actualizado')


@app.route('/actualizar-entrega-pre', methods = ['GET','POST'])
def actualizar_entrega_pre():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('actualizar-entrega-pre.html', data = data)
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        loaded = json.loads(data_json)
        if loaded[INPUT_ID] != ['']:
            idnum = loaded[INPUT_ID][0]
        data,materiales = filter_data_by('id',data_json)
        if data == False:
            data = get_all_data()
            return render_template('actualizar-entrega-pre.html', data = data, error = 'Faltan datos')
        return render_template('actualizar-entrega.html', data = data, error = 'Filtrado OK', materiales = materiales, idnum = idnum)


@app.route('/actualizar-entrega', methods = ['GET','POST'])
def actualizar_entrega():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('actualizar-entrega.html', data = data)
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)

        ret = update_data_by('entrega',data_json)
        if ret == False:
            data = get_all_data()
            return render_template('actualizar-entrega-pre.html', error = 'Falta datos', data = data)
            
        data = get_all_data()
        return render_template('actualizar-entrega-pre.html',data = data, error = 'Actualizado')

@app.route('/actualizar-proveedores', methods = ['GET','POST'])
def actualizar_proveedores():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('actualizar-proveedores.html', data = data)
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        loaded = json.loads(data_json)
        if loaded[INPUT_ID] != ['']:
            idnum = loaded[INPUT_ID][0]
        data,materiales = filter_data_by('id',data_json)
        if data == False:
            data = get_all_data()
            return render_template('actualizar-proveedores.html', data = data, error = 'Faltan datos')
        proveedores = get_proveedores()
        if proveedores == False:
            data = get_all_data()
            return render_template('actualizar-proveedores.html', data = data, error = 'Filtrado OK')
        return render_template('actualizar-proveedores-2.html', data = data, error = 'Filtrado OK', materiales = materiales, proveedores = proveedores,idnum = idnum)

@app.route('/actualizar-proveedores-2', methods = ['GET','POST'])
def actualizar_proveedores_2():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('actualizar-proveedores-2.html', data = data)
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        result,idnum = update_materials(data_json)

        if result == False:
            data = get_all_data()
            return render_template('actualizar-proveedores.html', data = data, error = 'Faltan datos')

        data,materiales = filter_updated(idnum)
        if data == False:
            data = get_all_data()
            return render_template('actualizar-proveedores.html', data = data, error = 'Faltan datos')
        
        proveedores = get_proveedores()
        if proveedores == False:
            data = get_all_data()
            return render_template('actualizar-proveedores.html', data = data, error = 'Filtrado OK')

        return render_template('actualizar-proveedores.html', data = data, error = 'Filtrado OK', materiales = materiales, proveedores = proveedores)
        

@app.route('/filtrar-id', methods = ['GET','POST'])
def filtrar_id():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('filtrar-id.html', data = data)
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        data,materiales = filter_data_by('id',data_json)
        if data == False:
            data = get_all_data()
            return render_template('filtrar-id.html', data = data, error = 'Faltan datos')
        return render_template('filtrar-id.html', data = data, error = 'Filtrado OK', materiales = materiales)
        

@app.route('/filtrar-obra', methods = ['GET','POST'])
def filtrar_obra():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('filtrar-obra.html', data = data)

    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        data,materiales = filter_data_by('obra',data_json)
        if data == False:
            data = get_all_data()
            return render_template('filtrar-obra.html', data = data, error = 'Faltan datos')
        return render_template('filtrar-obra.html', data = data, error = 'Filtrado OK')


@app.route('/filtrar-proveedor', methods = ['GET','POST'])
def filtrar_proveedor():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('filtrar-proveedor.html', data = data)

    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        data,materiales = filter_data_by('proveedor',data_json)
        if data == False:
            data = get_all_data()
            return render_template('filtrar-proveedor.html', data = data, error = 'Faltan datos')
        return render_template('filtrar-proveedor.html', data = data, error = 'Filtrado OK')


@app.route('/borrar', methods = ['GET','POST'])
def borrar():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('borrar.html', data = data)
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        if delete_from_database(data_json) == False:
            data = get_all_data()
            return render_template('borrar.html', error = 'Falta completar el ID', data = data)
        data = get_all_data()
        return render_template('borrar.html', error = 'Pedido borrado', data = data)

@app.route('/monitor', methods = ['GET','POST'])
def monitor():
    if request.method == 'GET':
        data = get_all_data(True)
        return render_template('monitor.html', data = data)

@app.route('/cargar-proveedor', methods = ['GET','POST'])
def proveedor():
    proveedores = []
    if request.method == 'GET':
        proveedores = proveedores_listed()
        return render_template('cargar-proveedor.html', data = proveedores)

    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)

        if is_toadd(data_json):
            if add_proveedor(data_json):
                proveedores = proveedores_listed()
                return render_template('cargar-proveedor.html',data = proveedores)
        else:
            if delete_proveedor(data_json):
                proveedores = proveedores_listed()
                return render_template('cargar-proveedor.html',data = proveedores)

        proveedores = proveedores_listed()
        return render_template('cargar-proveedor.html', data = proveedores)

@app.route('/cargar-obra', methods = ['GET','POST'])
def obra():
    obras = []
    if request.method == 'GET':
        obras = obras_listed()
        return render_template('cargar-obra.html', data = obras)

    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)

        if is_toadd(data_json):
            if add_obra(data_json):
                obras = obras_listed()
                return render_template('cargar-obra.html',data = obras)
        else:
            if delete_obra(data_json):
                obras = obras_listed()
                return render_template('cargar-obra.html',data = obras)
        
        obras = obras_listed()
        return render_template('cargar-obra.html',data = obras)


if __name__ == '__main__':

    # First create database if not exist
    if create_tables(DATABASE) == False:
        while True:
            c = 0

    # Run server
    run_simple('0.0.0.0',8000,app,use_reloader = True,use_debugger=True, use_evalex=True, reloader_interval=5, 
    reloader_type='auto',threaded=False, processes=1, request_handler=None, static_files=None, passthrough_errors=False, 
    ssl_context=None)