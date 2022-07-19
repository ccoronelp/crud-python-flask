from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os


app = Flask(__name__)
#conexión con base de datos
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='carlos'
app.config['MYSQL_DATABASE_PASSWORD']='123'
app.config['MYSQL_DATABASE_DB']='carlos'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

####************ sistema operativo
CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

#####-----------------/
@app.route('/')
def index():
    sql="SELECT * FROM `usuario`"

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    #después de ejecutar el cursor pasamos un fetchall para guardar en empleados
    empleados = cursor.fetchall()
    #print(empleados)
    conn.commit()

    return render_template('empleados/index.html',empleados=empleados)

#####-----------------/eliminando elemento
@app.route('/destroy/<int:id>')
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM usuario WHERE id=%s",id)
    conn.commit()

    return redirect('/')

#####-----------------/edit element
@app.route('/edit/<int:id>')
def edit(id):
    conn=mysql.connect()
    cursor=conn.cursor()   

    cursor.execute("SELECT * FROM usuario WHERE id=%s",id);
    empleados = cursor.fetchall()

    conn.commit()
#   print(empleados)
    return render_template('empleados/edit.html',empleados=empleados)

# recibiendo datos del formulario ubdate de edit.html
@app.route('/update', methods=['POST'])
def update():
    _id = request.form['txtID']
    _nombre = request.form['txtNombre']
    _correo = request.form['correo']
    _foto = request.files['foto']

    sql = "UPDATE `usuario` SET `nombre`=%s, `correo`=%s WHERE id=%s"
    datos = (_nombre,_correo,_id)

    conn = mysql.connect()
    cursor = conn.cursor()

    #Trabajamos la imagen
    now = datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    print (tiempo)

    if _foto.filename!='':
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

        cursor.execute("SELECT `foto` FROM `usuario` WHERE `id`=%s",_id)
        fila=cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE `usuario` SET `foto`=%s WHERE `id`=%s",(nuevoNombreFoto,_id))
        conn.commit()

    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')


#####-----------------/
@app.route('/create')
def create():
    return render_template('empleados/create.html')

#####-----------------/
#Recibiendo datos mediaten post del formulario create
@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['correo']
    _foto = request.files['foto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename!='' :
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql="INSERT INTO `usuario` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s)"
    datos = (_nombre,_correo,nuevoNombreFoto)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('empleados/index.html')

if __name__=='__main__':
    app.run(debug=True)

