from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = 'pc_parts.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cpus = conn.execute('SELECT * FROM cpus').fetchall()
    motherboards = conn.execute('SELECT * FROM motherboards').fetchall()
    ram = conn.execute('SELECT * FROM ram').fetchall()
    gpus = conn.execute('SELECT * FROM gpus').fetchall()
    power_supplies = conn.execute('SELECT * FROM power_supplies').fetchall()
    conn.close()
    return render_template('index.html', cpus=cpus, motherboards=motherboards, ram=ram, gpus=gpus, power_supplies=power_supplies)

@app.route('/check_compatibility', methods=['POST'])
def check_compatibility():
    cpu_id = request.form.get('cpu')
    motherboard_id = request.form.get('motherboard')
    ram_id = request.form.get('ram')
    gpu_id = request.form.get('gpu')
    power_supply_id = request.form.get('power_supply')

    conn = get_db_connection()

    cpu = conn.execute('SELECT * FROM cpus WHERE id = ?', (cpu_id,)).fetchone()
    motherboard = conn.execute('SELECT * FROM motherboards WHERE id = ?', (motherboard_id,)).fetchone()
    ram = conn.execute('SELECT * FROM ram WHERE id = ?', (ram_id,)).fetchone()
    gpu = conn.execute('SELECT * FROM gpus WHERE id = ?', (gpu_id,)).fetchone()
    power_supply = conn.execute('SELECT * FROM power_supplies WHERE id = ?', (power_supply_id,)).fetchone()

    conn.close()

    compatibility_errors = []

    # Проверка совместимости CPU и материнской платы
    if cpu and motherboard and cpu['socket'] != motherboard['socket']:
        compatibility_errors.append("CPU socket не совместим с материнской платой.")

    # Проверка совместимости RAM и материнской платы
    if motherboard and ram and motherboard['ram_type'] != ram['ram_type']:
        compatibility_errors.append("Тип RAM не совместим с материнской платой.")

    # Проверка достаточности мощности блока питания (пример)
    total_power_consumption = 0
    if gpu:
        total_power_consumption += gpu['power_consumption'] # Пример: потребление видеокарты
    if power_supply and power_supply['wattage'] < total_power_consumption:
        compatibility_errors.append("Недостаточная мощность блока питания для видеокарты.")


    if compatibility_errors:
        return render_template('results.html', errors=compatibility_errors, cpu=cpu, motherboard=motherboard, ram=ram, gpu=gpu, power_supply=power_supply) # Передаем выбранные комплектующие для отображения

    return render_template('results.html', errors=[], cpu=cpu, motherboard=motherboard, ram=ram, gpu=gpu, power_supply=power_supply)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/info')
def contact():
    return render_template('info.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')


if __name__ == '__main__':
    app.run(debug=True)


