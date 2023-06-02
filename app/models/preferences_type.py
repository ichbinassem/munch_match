from app.extensions import db

preferences_type = db.Table(
    "preferences_type",
    db.Column("preferences_id", db.Integer, db.ForeignKey("preferences.id")),
    db.Column("type_id", db.Integer, db.ForeignKey("type.id")),
)
