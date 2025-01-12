from flask import request, jsonify, send_file, url_for
from app import app
from app.pdf_generator import PDFGenerator
import os
from datetime import datetime
import tempfile

@app.route('/generate-invoice', methods=['POST'])
def generate_invoice():
    try:
        if not request.is_json:
            return jsonify({'error': 'Se requiere JSON'}), 400
            
        data = request.json
        generator = PDFGenerator()
        pdf_buffer = generator.generate_invoice(data)
        
        # Crear archivo temporal
        temp_dir = tempfile.gettempdir()
        filename = f"factura_{data['cliente']['nombre']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        temp_path = os.path.join(temp_dir, filename)
        
        with open(temp_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        # Crear URL de descarga
        download_url = request.host_url.rstrip('/') + url_for('download_pdf', filename=filename)
        
        return jsonify({
            'success': True,
            'download_url': download_url,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_pdf(filename):
    temp_dir = tempfile.gettempdir()
    return send_file(
        os.path.join(temp_dir, filename),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )