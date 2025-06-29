from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB = 'invoices.db'

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    quantities = conn.execute('SELECT * FROM quantities').fetchall()
    vehicles = conn.execute('SELECT * FROM vehicles').fetchall()
    conn.close()
    return render_template('index.html', items=items, customers=customers, quantities=quantities, vehicles=vehicles)

@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    data = request.json
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')
    conn = get_db_connection()
    conn.execute('INSERT INTO invoices (date, time, item_id, customer_id, quantity_id, vehicle_id, destination) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (date, time, data['item_id'], data['customer_id'], data['quantity_id'], data['vehicle_id'], data['destination']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/invoice_history')
def invoice_history():
    conn = get_db_connection()
    rows = conn.execute("SELECT i.*, it.name AS item, c.name AS customer, q.value AS quantity, v.number AS vehicle FROM invoices i JOIN items it ON i.item_id=it.id JOIN customers c ON i.customer_id=c.id JOIN quantities q ON i.quantity_id=q.id JOIN vehicles v ON i.vehicle_id=v.id WHERE date >= DATE('now', '-3 day')").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    app.run(debug=True)
