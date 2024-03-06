#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Configured database instance.
from config import db
# SQLAlchemy object validation tools.
from sqlalchemy.orm import validates
# SQLAlchemy object model serialization tools.
from sqlalchemy_serializer import SerializerMixin
# SQLAlchemy object association tools.
from sqlalchemy.ext.associationproxy import association_proxy


#######################################################
######## MODEL ASSOCIATION CONFIG INSTRUCTIONS ########
#######################################################


"""
There are three major steps to giving life to our association table.
(With an important preliminary step.)

0.  Ensure stability of our previously constructed "physical" objects.
        0a. Set up the table name and columns of the `Dog` database object model.
        0b. Set up the table name and columns of the `User` database object model.
        0c. Set up the table name and columns of the `Adoption` associative object model.

1.  Connect an individual physical object to the association table.
        1a. Construct a new relationship from dogs to adoptions.
                [ `Dog` <-> `Adoption` ]
        1b. Close the relationship from adoptions back to dogs.
                [ `Adoption` <-> `Dog` ]
        1c. Construct a new relationship from users to adoptions.
                [ `User` <-> `Adoption` ]
        1d. Close the relationship from adoptions back to users.
                [ `Adoption` <-> `User` ]

2.  Link each physical object association to the OTHER corresponding physical object.
        2a. Construct an association proxy that links the dog-adoption relationship 
            to the user-adoption relationship.
                [ (`Dog` <-> `Adoption`) <–––> (`Biome` <-> `Adoption`) ]
        2b. Construct an association proxy that links the user-adoption relationship
            to the dog-adoption relationship.
                [ (`Biome` <-> `Adoption`) <–––> (`Dog` <-> `Adoption`) ]

3.  Instruct our program(s) at every chance we get (both in `models.py` and `app.py`)
    to not infinitely recurse/cascade when accessing nested data, using a technique
    called "serialization rules".
        3a. Design serialization rules for the dog table to avoid cascading when
            accessing dog data via adoption table traversal.
        3b. Design serialization rules for the user table to avoid cascading when
            accessing user data via adoption table traversal.
        3c. Design serialization rules for the adoption table to avoid cascading when
            accessing adoption data from the dog table.
        3d. Design serialization rules for the adoption table to avoid cascading when
            accessing adoption data from the user table.
"""


#######################################################
######### RELATIONAL DATABASE OBJECT MODEL(S) #########
#######################################################


# Database object model definition for dog(s).
# NOTE: This needs to be subclassed with two superclasses.
#   -> `db.Model` for SQL-like database structuring.
#   -> `SerializerMixin` for data serialization and avoiding infinite referencing.
class Dog(db.Model, SerializerMixin):
    # 0a.   Set up name of SQL database table containing dog data.
    __tablename__ = "dog_table"

    # 0a.   Set up physical object columns prior to interdependent association(s).
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    breed = db.Column(db.String, nullable=False)
    # photo = db.Column(db.String, nullable=False)
    is_adoptable = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # 1a.   Create a relationship that links a dog row to an adoption row.
    # NOTE: This relationship sets up the connection from a dog to an adoption, 
    #       and must be closed from an adoption back to a dog. 
    adoptions = db.relationship("Adoption", back_populates="dog")

    # 2a.   Create an association proxy from the dog-adoption relationship 
    #       to the user-adoption relationship.
    users = association_proxy("adoptions", "user")

    # 3a.   Create serialization rules to avoid infinite cascading/recursion
    #       when accessing dog data from an adoption.
    serialize_rules = ("-adoptions.dog",)


# Database object model definition for user(s).
# NOTE: This needs to be subclassed with two superclasses.
#   -> `db.Model` for SQL-like database structuring.
#   -> `SerializerMixin` for data serialization and avoiding infinite referencing.
# NOTE: `User.password` must be cryptographically hashed prior to database storage.
class User(db.Model, SerializerMixin):
    # 0b.   Set up name of SQL database table containing user data.
    __tablename__ = "user_table"

    # 0b.   Set up physical object columns prior to interdependent association(s).
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def is_administrator(self):
        return self.is_admin
    
    # 1c.   Create a relationship that links a user row to an adoption row.
    # NOTE: This relationship sets up the connection from a user to an adoption, 
    #       and must be closed from an adoption back to a user.
    adoptions = db.relationship("Adoption", back_populates="user")

    # 2b.   Create an association proxy from the user-adoption relationship
    #       to the dog-adoption relationship.
    dogs = association_proxy("adoptions", "dog")

    # 3b.   Create serialization rules to avoid infinite cascading/recursion 
    #       when accessing user data from an adoption.
    serialize_rules = ("-adoptions.user",)
    

# Database association model definition for connecting a dog and a user.
# NOTE: This needs to be subclassed with two superclasses.
#   -> `db.Model` for SQL-like database structuring.
#   -> `SerializerMixin` for data serialization and avoiding infinite referencing.
class Adoption(db.Model, SerializerMixin):
    # 0c.   Set up name of SQL database table containing adoption data.
    __tablename__ = "adoption_table"

    # 0c.   Set up association object columns prior to dependent association(s).
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey("dog_table.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # 1b.   Extend the relationship from (1a) to link from an adoption row back to a dog row.
    # NOTE: This relationship is the secondary piece that closes the loop from a dog to an adoption
    #       by connecting an adoption back to a dog.
    dog = db.relationship("Dog", back_populates="adoptions")

    # 1d.   Extend the relationship from (1c) to link from an adoption row back to a user row.
    # NOTE: This relationship is the secondary piece that closes the loop from a user to an adoption
    #       by connecting an adoption back to a user.
    user = db.relationship("User", back_populates="adoptions")

    # 3c.   Create serialization rules to avoid infinite cascading/recursion
    #       when accessing adoption data from a dog.
    # 3d.   Create serialization rules to avoid infinite cascading/recursion 
    #       when accessing adoption data from a user.
    serialize_rules = ("-dog.adoptions", "-user.adoptions")