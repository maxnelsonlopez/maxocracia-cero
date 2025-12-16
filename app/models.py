from datetime import datetime

from .extensions import db


class User(db.Model):  # type: ignore
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    alias = db.Column(db.String(50))
    password_hash = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    city = db.Column(db.String(50))
    neighborhood = db.Column(db.String(50))
    values_json = db.Column(db.Text)  # JSON stored as text in SQLite
    created_at = db.Column(db.String(30), default=datetime.utcnow().isoformat)

    def __repr__(self):
        return f"<User {self.email}>"


class Participant(db.Model):  # type: ignore
    """Formulario CERO - Participantes"""

    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    referred_by = db.Column(db.String(100))
    phone_call = db.Column(db.String(20))
    phone_whatsapp = db.Column(db.String(20))
    telegram_handle = db.Column(db.String(50))
    city = db.Column(db.String(50), nullable=False)
    neighborhood = db.Column(db.String(50), nullable=False)
    personal_values = db.Column(db.Text)

    # JSON fields stored as Text
    offer_categories = db.Column(db.Text)
    offer_description = db.Column(db.Text, nullable=False)
    offer_human_dimensions = db.Column(db.Text)

    need_categories = db.Column(db.Text)
    need_description = db.Column(db.Text, nullable=False)
    need_urgency = db.Column(db.String(10))
    need_human_dimensions = db.Column(db.Text)

    consent_given = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default="active")
    created_at = db.Column(db.String(30), default=datetime.utcnow().isoformat)

    def __repr__(self):
        return f"<Participant {self.name}>"


class Interchange(db.Model):  # type: ignore
    """Formulario A - Intercambios"""

    __tablename__ = "interchange"

    id = db.Column(db.Integer, primary_key=True)
    interchange_id = db.Column(db.String(36), unique=True)
    date = db.Column(db.String(30))

    giver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    giver = db.relationship(
        "User", foreign_keys=[giver_id], backref="given_interchanges"
    )
    receiver = db.relationship(
        "User", foreign_keys=[receiver_id], backref="received_interchanges"
    )

    type = db.Column(db.String(50))
    description = db.Column(db.Text)
    urgency = db.Column(db.String(20))

    uth_hours = db.Column(db.Float)
    impact_resolution_score = db.Column(db.Integer)

    # VHV Data
    uvc_score = db.Column(db.Float)
    urf_units = db.Column(db.Float)
    vhv_time_seconds = db.Column(db.Float)
    vhv_lives = db.Column(db.Float)
    vhv_resources_json = db.Column(db.Text)

    reciprocity_status = db.Column(db.String(50))
    requires_followup = db.Column(db.Integer, default=0)
    followup_scheduled_date = db.Column(db.String(30))

    created_at = db.Column(db.String(30), default=datetime.utcnow().isoformat)

    def __repr__(self):
        return f"<Interchange {self.interchange_id}>"


class FollowUp(db.Model):  # type: ignore
    """Formulario B - Seguimiento"""

    __tablename__ = "follow_ups"

    id = db.Column(db.Integer, primary_key=True)
    follow_up_date = db.Column(db.String(30))

    participant_id = db.Column(db.Integer, db.ForeignKey("participants.id"))
    participant = db.relationship("Participant", backref="follow_ups")

    related_interchange_id = db.Column(db.Integer, db.ForeignKey("interchange.id"))
    interchange = db.relationship("Interchange")

    follow_up_type = db.Column(db.String(50))
    current_situation = db.Column(db.Text)
    situation_change = db.Column(db.String(50))
    follow_up_priority = db.Column(db.String(20))

    created_at = db.Column(db.String(30), default=datetime.utcnow().isoformat)

    def __repr__(self):
        return f"<FollowUp {self.id} - {self.follow_up_priority}>"


class VHVProduct(db.Model):  # type: ignore
    __tablename__ = "vhv_products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    maxo_price = db.Column(db.Float)
    vhv_json = db.Column(db.Text)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    creator = db.relationship("User")

    def __repr__(self):
        return f"<VHVProduct {self.name}>"
