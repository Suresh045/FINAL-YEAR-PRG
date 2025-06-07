from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    User model for storing user credentials and admin status.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    applications = db.relationship('HouseApplication', backref='user', lazy=True)
    approved_houses = db.relationship('ApprovedHouse', backref='user', lazy=True)
    modifications = db.relationship('ModificationRequest', backref='user_modifications', lazy=True)  # Renamed backref to avoid conflict

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}, Admin: {self.is_admin}>"

class House(db.Model):
    """
    House model to store house details such as owner name, coordinates, and satellite image.
    """
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    satellite_image = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<House {self.owner_name} at ({self.latitude}, {self.longitude})>"

class HouseApplication(db.Model):
    """
    House Application model to store information about applications for house approval.
    """
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)  # ✅ Add this
    email = db.Column(db.String(120), nullable=False)        # ✅ Add this
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    house_address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="Pending")  # 'Pending', 'Approved', 'Rejected'
    rejection_reason = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Add this line for satellite image
    satellite_image = db.Column(db.String(255), nullable=True)  # This will hold the filename or path

    def __repr__(self):
        return f"<HouseApplication {self.owner_name} - {self.status}>"


class ApprovedHouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)  # ✅ NEW
    email = db.Column(db.String(120), nullable=False)         # ✅ NEW
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    satellite_image = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<ApprovedHouse {self.owner_name} at ({self.latitude}, {self.longitude})>"


class RejectedHouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)  # ✅ NEW
    email = db.Column(db.String(120), nullable=False)         # ✅ NEW
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    satellite_image = db.Column(db.String(100), nullable=True)
    rejection_reason = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<RejectedHouse {self.owner_name}>"


class ConstructionDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer)
    owner_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))  # ✅ NEW
    email = db.Column(db.String(120))        # ✅ NEW
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    address = db.Column(db.String(200))
    new_image = db.Column(db.String(200))
    modified_last_year = db.Column(db.String(10))
    changes_detected = db.Column(db.String(10))
    status = db.Column(db.String(10))  # ✅ NEW
    def __repr__(self):
        return f'<ConstructionDetail {self.id}>'



class ModificationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    house_id = db.Column(db.Integer, db.ForeignKey('approved_house.id'))  # Link to approved house

    house_name = db.Column(db.String(100))
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    address = db.Column(db.Text)
    reason = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending')

    user = db.relationship('User', backref='modifications_requests')
    # 'approved_house' backref automatically created from ApprovedHouse

    def __repr__(self):
        return f"<ModificationRequest {self.house_name}, Status: {self.status}>"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    feedback_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)  # NEW FIELD
