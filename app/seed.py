from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

fake = Faker()

VALID_STRENGTH_VALUES = ["Strong", "Weak", "Average"]

def generate_fake_hero():
    return Hero(
        name=fake.first_name(),
        super_name=fake.word() + "man",  
    )

def generate_fake_power():
    return Power(
        name=fake.word(),
        description=fake.sentence(),
    )

def generate_fake_hero_power(hero, power):
    return HeroPower(
        hero=hero,
        power=power,
        strength=fake.random_element(elements=VALID_STRENGTH_VALUES),
    )

def seed_database():
    with app.app_context():
        db.create_all()

        # Generate fake heroes and powers
        heroes = [generate_fake_hero() for _ in range(10)]
        powers = [generate_fake_power() for _ in range(5)]

        db.session.add_all(heroes)
        db.session.add_all(powers)
        db.session.commit()

        print("Fake heroes and powers generated and added to the database.")

        # Assign random powers to random heroes
        for hero in heroes:
            for _ in range(fake.random_int(min=1, max=3)):
                power = fake.random_element(elements=powers)
                hero_power = generate_fake_hero_power(hero, power)
                db.session.add(hero_power)

        db.session.commit()

        print("Random powers assigned to random heroes. Database seeding complete.")

if __name__ == "__main__":
    seed_database()
