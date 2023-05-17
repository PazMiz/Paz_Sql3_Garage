from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

sqliteConnection = sqlite3.connect('sql.db', check_same_thread=False)
cursor = sqliteConnection.cursor()

# Creating table
table = """
    CREATE TABLE IF NOT EXISTS Garage(
        ClientName VARCHAR(255),
        carName VARCHAR(255),
        Model VARCHAR(255),
        Fix VARCHAR(255)
    );
"""
cursor.execute(table)


@app.route('/')
def home():

    data = cursor.execute('SELECT rowid, * FROM Garage').fetchall()
    return render_template('index.html', msg=data)


@app.route('/newcar', methods=['GET', 'POST'])
def NewGarage():
    if request.method == 'POST':
        ClientName = request.form.get('ClientName')
        carName = request.form.get('carName')
        Model = request.form.get('Model')
        Fix = request.form.get('Fix')

        cursor.execute(
            "INSERT INTO Garage(ClientName, carName, Model, Fix) VALUES (?, ?, ?, ?)",
            (ClientName, carName, Model, Fix))

        sqliteConnection.commit()

        variables = {
            'ClientName': ClientName,
            'carName': carName,
            'Model': Model,
            'Fix': Fix
        }
        return render_template('index.html', msg=[variables])

    return render_template('newcar.html')


@app.route('/updatecar/<int:id>', methods=['GET', 'POST'])
def updatecar(id):

    if request.method == 'POST':
        ClientName = request.form.get('ClientName')
        carName = request.form.get('carName')
        Model = request.form.get('Model')
        Fix = request.form.get('Fix')

        cursor.execute(
            "UPDATE Garage SET ClientName=?, carName=?, Model=?, Fix=? WHERE rowid=?",
            (ClientName, carName, Model, Fix, id)
        )
        sqliteConnection.commit()

        return '''
            <h1>Record updated successfully</h1>
            <a href="/">Go back to home page</a>
        '''

    record = cursor.execute(
        "SELECT * FROM Garage WHERE rowid=?", (id,)).fetchone()

    return render_template('updatecar.html', record=record)


@app.route('/deletecar/<int:id>', methods=['POST'])
@app.route('/deletecar/<int:id>')
def deletecar(id):
    cursor.execute("DELETE FROM Garage WHERE rowid=?", (id,))
    sqliteConnection.commit()

    return '''
        <h1>Record deleted successfully</h1>
        <a href="/">Go back to home page</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)