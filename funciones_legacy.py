@app.route('/filtrar', methods = ['GET','POST'])
def filtrar():
    if request.method == 'GET':
        data = get_all_data()
        return render_template('filtrar.html', data=data)
    
    if request.method == 'POST':
        global option
        info = request.form.to_dict(flat=False)
        data_json = json.dumps(info)
        loaded = json.loads(data_json)
        print(data_json)
        
        # Take de filter id to refresh page later
        if INPUT_ID in loaded:
            if loaded[INPUT_ID] != ['']:
                option = loaded[INPUT_ID][0]
        if 'proveedores' in loaded:
            print('Proveedores available')

        data,materiales = filter_from_database(option,data_json)
        if data == False:
            data = get_all_data()
            return render_template('filtrar.html', data = data, error = 'Faltan datos')

        if not materiales or not data:
            return render_template('filtrar.html', data = data, error = 'Filtrado OK')
        
        proveedores = get_proveedores()
        if proveedores == False:
            data = get_all_data()
            return render_template('filtrar.html', data = data, error = 'Filtrado OK')

        return render_template('filtrar.html', data = data, error = 'Filtrado OK', materiales = materiales, proveedores = proveedores)