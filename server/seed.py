#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Configured application/server and database instances.
from config import db, app
# Relative access to user, dog, and adoption models.
from models import User, Dog, Adoption

# Cryptographic hashing tools for user authentication.
import bcrypt

# Random selection tools.
from random import choice


#######################################################
########## DEFINING DATA SEEDING FUNCTION(S) ##########
#######################################################


# Helper function to generate sample users using relevant object model.
def create_users():
    # Inner function to handle cryptographic hashing of passwords for safer database storage.
    def encrypt_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)
        return hashed_password.decode("utf-8")
    
    user_1 = User(username="friendly_neighborhood_user", password=encrypt_password("hunter2"))
    user_2 = User(username="into_the_userverse", password=encrypt_password("drowssap"))
    user_3 = User(username="amazing_administrator", password=encrypt_password("abcde12345"), is_admin=True)
    
    return [user_1, user_2, user_3]

# Helper function to generate sample dogs using relevant object model.
def create_dogs():
    dog_1 = Dog(name="Odie", breed="Beagle")
    dog_2 = Dog(name="Benji", breed="Basenji")
    dog_3 = Dog(name="Fido", breed="Irish Wolfhound")
    dog_4 = Dog(name="Rex", breed="Rottweiler")
    dog_5 = Dog(name="Skipper", breed="Malamute")
    dog_6 = Dog(name="Zoomer", breed="Viszla", is_adoptable=False)
    dog_7 = Dog(name="Borky", breed="Pomeranian", is_adoptable=False)
    dog_8 = Dog(name="Ghost", breed="Siberian Husky", is_adoptable=False)

    return [dog_1, dog_2, dog_3, dog_4, dog_5, dog_6, dog_7, dog_8]

# Helper function to curate several sample adoptions (dog-user associations).
def create_adoptions(sample_users, sample_dogs):
    general_users = [user for user in sample_users if user.is_admin is False]
    adopted_dogs = [dog for dog in sample_dogs if dog.is_adoptable is False]
    sample_adoptions = []
    for adopted_dog in adopted_dogs:
        sample_adoptions.append(Adoption(
            dog_id=adopted_dog.id,
            user_id=choice(general_users).id
        ))
    return sample_adoptions

#######################################################
#### DATABASE POPULATION WITHIN APPLIATION CONTEXT ####
#######################################################


with app.app_context():
    print(">> Seeding data...")

    print("\n\t>> Deleting preexisting table data...")
    User.query.delete()
    Dog.query.delete()
    Adoption.query.delete()
    db.session.commit()
    print("\t>> Data deletion successful.")

    print("\n\t>> Generating sample data for users with cryptographic hashing...")
    sample_users = create_users()
    db.session.add_all(sample_users)
    db.session.commit()
    print("\t>> User data generation successful.")

    print("\n\t>> Generating sample data for dogs...")
    sample_dogs = create_dogs()
    db.session.add_all(sample_dogs)
    db.session.commit()
    print("\t>> Dog data generation successful.")

    print("\n\t>> Generating random associations (adoptions) between relevant users and dogs...")
    sample_adoptions = create_adoptions(sample_users=sample_users, sample_dogs=sample_dogs)
    db.session.add_all(sample_adoptions)
    db.session.commit()
    print("\t>> Adoption association generation successful.")

    print("\n>> Data seeding complete.")