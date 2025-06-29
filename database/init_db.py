import sqlite3

conn = sqlite3.connect('../invoices.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
    item_id INTEGER,
    customer_id INTEGER,
    quantity_id INTEGER,
    vehicle_id INTEGER,
    destination TEXT
)''')

for table, values in {
    'items': ['Sand', 'Gravel'],
    'customers': ['ABC Constructions', 'XYZ Ltd.'],
    'quantities': ['1 Ton', '2 Tons'],
    'vehicles': ['MH12AB1234', 'MH14XY5678']
}.items():
    c.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)" if table != 'quantities' and table != 'vehicles' else
              f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, {'value' if table=='quantities' else 'number'} TEXT UNIQUE)")
    for v in values:
        try:
            c.execute(f"INSERT INTO {table} ({'name' if table != 'quantities' and table != 'vehicles' else 'value' if table == 'quantities' else 'number'}) VALUES (?)", (v,))
        except:
            pass  # skip duplicates

conn.commit()
conn.close()
