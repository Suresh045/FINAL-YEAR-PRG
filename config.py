import os  # ✅ Add this line

class Config:
    SECRET_KEY = "suresh123"  # Secret Key for Session Security
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"  # SQLite Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Fix: Define UPLOAD_FOLDER properly
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')

    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'governmentconstructionfindout@gmail.com'
    MAIL_PASSWORD = 'xhihcvisfwyfaxiu'  # ✅ App Password (no spaces)
    MAIL_DEFAULT_SENDER = 'governmentconstructionfindout@gmail.com'  # Default sender email

    # Other configurations can go here if needed
