import sqlite3

def insert_letter(contract_number, order_number, date, time, contractor, FIO, subject, status, type_of_letter):
    conn = sqlite3.connect("letters.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(type_id) FROM outgoing_letters WHERE type = ?", (type_of_letter,))
    max_type_id = cursor.fetchone()[0]
    next_type_id = (max_type_id or 0) + 1
    cursor.execute("""
        INSERT INTO outgoing_letters (
            type, type_id, contract_number, order_number, date, time, contractor, FIO, subject, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (type_of_letter, next_type_id, contract_number, order_number, date, time, contractor, FIO, subject, status))

    conn.commit()
    conn.close()
    return next_type_id
