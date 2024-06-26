import hashlib
import uuid
import os
from werkzeug.utils import secure_filename
from models import File
from app import db, app

class FileSaver:
    def __init__(self, file):
        self.file = file

    def save_to_db(self):
        self.img = self._find_by_md5_hash()
        if self.img is not None:
            return self.img
        file_name = secure_filename(self.file.filename)
        self.img = File(
            id=str(uuid.uuid4()),
            file_name=file_name,
            mime_type=self.file.mimetype,
            hash=self.md5_hash)
        db.session.add(self.img)
        return self.img
    
    def save_to_system(self):
        if self.img is not None:
            self.file.save(
                os.path.join(app.config['UPLOAD_FOLDER'],
                            self.img.storage_filename))
        return self.img

    def save(self):
        self.img = self._find_by_md5_hash()
        if self.img is not None:
            return self.img
        file_name = secure_filename(self.file.filename)
        self.img = File(
            id=str(uuid.uuid4()),
            file_name=file_name,
            mime_type=self.file.mimetype,
            hash=self.md5_hash)
        self.file.save(
            os.path.join(app.config['UPLOAD_FOLDER'],
                         self.img.storage_filename))
        db.session.add(self.img)
        db.session.commit()
        return self.img

    def _find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return db.session.execute(db.select(File).filter(File.hash == self.md5_hash)).scalar()
