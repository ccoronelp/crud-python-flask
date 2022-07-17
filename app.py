from flask import Flask
from flask import render_template,request
from flaskext.mysql import MySQL
from datetime import datetime


app = Flask(__name__)
#conexión con base de datos
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='carlos'
app.config['MYSQL_DATABASE_PASSWORD']='123'
app.config['MYSQL_DATABASE_DB']='carlos'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

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

