from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sqlite3
import os

pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))

def generate_pdf_by_type(db_path, output_pdf, letter_type):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT contract_number, type_id, date, time, contractor, FIO, subject, status
        FROM outgoing_letters
        WHERE type = ?
        ORDER BY type_id
    """, (letter_type,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"❗Нет писем с типом: {letter_type}")
        return

    c = canvas.Canvas(output_pdf, pagesize=A3)
    width, height = A3
    c.setFont("DejaVu", 10)

    headers = ["№ письма", "Дата", "Время", "Контрагент", "ФИО исполнителя", "Тема письма", "Статус"]
    col_widths = [30*mm, 30*mm, 25*mm, 50*mm, 45*mm, 70*mm, 35*mm]
    x_start = 7.5 * mm
    y_start = height - 30 * mm
    y = y_start

    def draw_table_header():
        nonlocal y
        x = x_start
        c.setFont("DejaVu", 10)
        for header, col_width in zip(headers, col_widths):
            c.rect(x, y, col_width, 10*mm)
            c.drawString(x + 2*mm, y + 3*mm, header)
            x += col_width
        y -= 10*mm

    draw_table_header()

    for row in rows:
        contract_number, type_id, date, time, contractor, FIO, subject, status = row
        if y < 30 * mm:
            c.showPage()
            y = y_start
            draw_table_header()

        values = [
            f"{contract_number}/{type_id}",
            date,
            time,
            contractor,
            FIO,
            subject,
            status
        ]

        x = x_start
        for val, col_width in zip(values, col_widths):
            c.rect(x, y, col_width, 10*mm)
            c.drawString(x + 2*mm, y + 3*mm, str(val))
            x += col_width
        y -= 10*mm

    c.save()
    print(f"✅ PDF для типа '{letter_type}' создан: {output_pdf}")
