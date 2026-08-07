import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_uploaded_image(file_storage, folder_name='products') -> str:
    """Saves uploaded image safely and returns relative static path."""
    if not file_storage or not file_storage.filename:
        return None

    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    if ext not in current_app.config['ALLOWED_EXTENSIONS']:
        return None

    import uuid
    unique_filename = f"{uuid.uuid4().hex[:12]}_{filename}"
    
    target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
    os.makedirs(target_dir, exist_ok=True)
    
    filepath = os.path.join(target_dir, unique_filename)
    file_storage.save(filepath)
    
    return f"uploads/{folder_name}/{unique_filename}"
