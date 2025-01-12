from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
import os
from io import BytesIO
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.width, self.height = A4

    def generate_invoice(self, data):
        # Crear buffer en memoria
        buffer = BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        
        story = []
        styles = getSampleStyleSheet()

        # Título FACTURA
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Normal'],
            fontSize=16,
            alignment=1,
            spaceAfter=10*mm
        )
        story.append(Paragraph("FACTURA", title_style))
        
        # Línea horizontal después del título
        grey_line1 = Table([['']], colWidths=[170*mm], rowHeights=[0.5])
        grey_line1.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(grey_line1)
        story.append(Spacer(1, 5*mm))
        
        # Logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "img", "logo.png")
        if os.path.exists(logo_path):
            im = Image(logo_path, width=80*mm, height=25*mm)
            im.hAlign = 'CENTER'
            story.append(im)
        
        # Dirección empresa
        address_style = ParagraphStyle(
            'Address',
            parent=styles['Normal'],
            fontSize=10,
            alignment=1,
            textColor=colors.gray,
            spaceAfter=5*mm
        )
        story.append(Paragraph("David Cervera, cervantes 22, 46191 valencia, España", address_style))
        
        # Línea horizontal después de la dirección
        grey_line2 = Table([['']], colWidths=[170*mm], rowHeights=[0.5])
        grey_line2.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(grey_line2)
        story.append(Spacer(1, 10*mm))

        # Información del cliente
        data_table = [
            ['Cliente:', data['cliente']['nombre'], 'NºFactura:', data['factura']['numero']],
            ['Dirección:', data['cliente']['direccion'].split('\n')[0], 'Fecha emisión:', data['factura']['fecha_emision']],
            ['', data['cliente']['direccion'].split('\n')[1], 'Vencimiento:', data['factura']['fecha_vencimiento']],
            ['CIF/NIF:', data['cliente']['DNI'], '', '']
        ]
        
        client_table = Table(data_table, colWidths=[20*mm, 80*mm, 30*mm, 40*mm])
        client_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(client_table)
        story.append(Spacer(1, 10*mm))

        # Tabla de conceptos
        items_data = [['Descripción', 'Cantidad', 'Precio']]
        total = 0
        for item in data['conceptos']:
            importe = item['cantidad'] * item['precio_unitario']
            total += importe
            items_data.append([
                item['descripcion'],
                str(item['cantidad']),
                f"{item['precio_unitario']:.2f}€"
            ])

        items_table = Table(items_data, colWidths=[110*mm, 30*mm, 30*mm])
        items_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 10*mm))

        # Totales
        iva = total * 0.21
        total_con_iva = total + iva
        totals_data = [
            ['Total sin IVA', f"{total:.2f}€"],
            ['IVA 21%', f"{iva:.2f}€"],
            ['TOTAL (EUR)', f"{total_con_iva:.2f}€"]
        ]
        
        totals_table = Table(totals_data, colWidths=[150*mm, 20*mm])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(totals_table)

        # Espacio antes de los datos de contacto
        story.append(Spacer(1, 50*mm))

        # Línea horizontal antes de los datos de contacto
        grey_line3 = Table([['']], colWidths=[170*mm], rowHeights=[0.5])
        grey_line3.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(grey_line3)
        story.append(Spacer(1, 5*mm))

        # Datos de contacto en tres líneas separadas
        contact_data = [
            ['David Cervera, cervantes 22, 46191 valencia, España', 'CIF/NIF: 73659624P', 'Persona de contacto David Cervera', 'Móvil 684022975'],
            ['E-mail davidcerverausedo@hotmail.com', 'Titular de la cuenta: David Cervera', 'Banco: CaixaBank', ''],
            ['IBAN: ES14 2100 7915 1713 0019 4098', '', '', '']
        ]
        
        contact_table = Table(contact_data, colWidths=[70*mm, 45*mm, 45*mm, 20*mm], rowHeights=[12, 12, 12])
        contact_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(contact_table)

        # Generar PDF en memoria
        doc.build(story)
        buffer.seek(0)
        return buffer
        # ... (resto del código igual)

        # Logo - con mejor manejo de errores y logging
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "img", "logo.png")
        print(f"Buscando logo en: {logo_path}")  # Para debugging
        
        if os.path.exists(logo_path):
            try:
                im = Image(logo_path, width=80*mm, height=25*mm)
                im.hAlign = 'CENTER'
                story.append(im)
            except Exception as e:
                print(f"Error al cargar el logo: {str(e)}")
        else:
            print(f"Logo no encontrado en {logo_path}")
            # Opcional: Añadir un espacio o texto en lugar del logo
            story.append(Spacer(1, 25*mm))

# ... (resto del código igual)
