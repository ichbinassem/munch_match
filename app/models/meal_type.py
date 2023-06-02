from app.extensions import db

meal_type = db.Table('meal_type',
                    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id')),
                    db.Column('type_id', db.Integer, db.ForeignKey('type.id'))
                    )