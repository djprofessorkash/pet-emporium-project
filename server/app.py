#######################################################
############## IMPORTS AND INSTANTIATIONS #############
#######################################################


# Flask server request-response and session storage utilities.
from flask import request, make_response, session
# Configured application/server and database instances.
from config import app, db
# Relative access to user and dog models.
from models import User, Dog
# Custom authorization decorator middleware.
from middleware import authorization_required

# Cryptographic hashing tools for user authentication.
import bcrypt


#######################################################
######## INITIAL SETUP ROUTES FOR APPLICATION #########
#######################################################


# GET route to access homepage.
# NOTE: No authentication required.
@app.route("/")
def root():
    return make_response({"msg": "Application loaded successfully.",
                          "notice": "To enter the API, please log in or create an account."}, 200)

# GET route to access API entrypoint.
# NOTE: Requires user privileges. (Can use decorator middleware.)
@app.route("/api")
@authorization_required
def api(current_user):
    return make_response({"user_id": current_user["id"],
                          "msg": "API access granted."}, 200)


#######################################################
######### APPLICATION CREDENTIAL VERIFICATION #########
#######################################################


# GET route to verify authentication.
@app.route("/api/check_session")
def verify_session():
    user = db.session.get(User, session.get("user_id"))
    if user is not None:
        return user.to_dict(), 200
    else:
        return {"msg": "No user logged in."}, 401


#######################################################
############ INITIAL SETUP ROUTES FOR DOGS ############
#######################################################


# GET route to view all dogs.
# NOTE: Requires user privileges. (Can use decorator middleware.)
@app.route("/api/dogs")
@authorization_required
def view_all_dogs(current_user):
    # Query all dog rows from database.
    all_dogs = [dog.to_dict(only=("id", "name", "breed")) for dog in Dog.query.all()]
    return make_response(all_dogs, 200)

# GET route to view all adoptable dogs.
# NOTE: Requires user privileges. (Can use decorator middleware.)
@app.route("/api/adopt")
@authorization_required
def view_adoptable_dogs(current_user):
    # Query all dog rows from database.
    all_dogs = Dog.query.all()

    # Convert all adoptable dogs to JSON-friendly object array as server output.
    adoptable_dogs = [dog.to_dict(only=("id", "name", "breed")) for dog in all_dogs if dog.is_adoptable is True]
    return make_response(adoptable_dogs, 200)

# GET route to view individual dog by ID.
# NOTE: Requires user privileges. (Can use decorator middleware.)
@app.route("/api/dogs/<int:dog_id>")
@authorization_required
def view_dog_by_id(current_user, dog_id: int):
    # Query and return dog from database that matches given ID.
    matching_dog = Dog.query.filter(Dog.id == dog_id).first()
    if not matching_dog:
        return make_response({"error": f"Dog ID `{dog_id}` not found in database."}, 404)
    return make_response(matching_dog.to_dict(only=("id", "name", "breed")), 200)


#######################################################
######### ADMINISTRATOR-ONLY ROUTES FOR DOGS ##########
#######################################################


# POST route to add new dog to database.
# NOTE: Requires administrative privileges. (Can use decorator middleware.)
@app.route("/api/dogs", methods=["POST"])
@authorization_required(methods=["POST"])
def add_dog(current_user):
    # Extract JSONified payload from request.
    payload = request.get_json()

    # Unpack payload attributes to new dog object.
    new_dog = Dog(
        name=payload["name"], 
        breed=payload["breed"],
        is_adoptable=True
    )

    # Add and commit new dog to database.
    db.session.add(new_dog)
    db.session.commit()
    return make_response(new_dog.to_dict(only=("id", "name", "breed")), 201)

# PATCH route to edit dog's information in database.
# NOTE: Requires administrative privileges. (Can use decorator middleware.)
@app.route("/api/dogs/<int:dog_id>", methods=["PATCH"])
@authorization_required(methods=["PATCH"])
def update_dog(current_user, dog_id: int):
    # Query dog from database that matches given ID.
    matching_dog = Dog.query.filter(Dog.id == dog_id).first()
    if not matching_dog:
        return make_response({"error": f"Dog ID `{dog_id}` not found in database."}, 404)
    
    # Extract JSONified payload from request.
    payload = request.get_json()

    # Iteratively update relevant dog attributes using payload data.
    for attribute in payload:
        setattr(matching_dog, attribute, payload[attribute])

    # Add and commit updated dog to database.
    db.session.add(matching_dog)
    db.session.commit()
    return make_response(matching_dog.to_dict(only=("id", "name", "breed")), 200)

# DELETE route to remove dog from database.
# NOTE: Requires administrative privileges. (Can use decorator middleware.)
@app.route("/api/dogs/<int:dog_id>", methods=["DELETE"])
@authorization_required(methods=["DELETE"])
def remove_dog(current_user, dog_id: int):
    # Query dog from database that matches given ID.
    matching_dog = Dog.query.filter(Dog.id == dog_id).first()
    if not matching_dog:
        return make_response({"error": f"Dog ID `{dog_id}` not found in database."}, 404)

    # Remove and commit dog from database.
    db.session.delete(matching_dog)
    db.session.commit()
    return make_response(matching_dog.to_dict(only=("id", "name", "breed")), 204)


#######################################################
############# USER AUTHENTICATION ROUTING #############
#######################################################


# POST route to add new user to database.
@app.route("/signup", methods=["POST"])
def add_user():
    if request.method == "POST":
        # Retrieve POST request as JSONified payload.
        payload = request.get_json()

        # Extract username and password from payload.
        username = payload["username"]
        password = payload["password"]

        # Generate salt for strenghening password encryption.
        # NOTE: Salts add additional random bits to passwords prior to encryption.
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)

        # Create new user instance using username and hashed password.
        new_user = User(
            username=username,
            password=hashed_password.decode("utf-8")
        )

        if new_user is not None:
            # Add and commit newly created user to database.
            db.session.add(new_user)
            db.session.commit()

            # Save created user ID to server-persistent session storage.
            # NOTE: Sessions are to servers what cookies are to clients.
            # NOTE: Server sessions are NOT THE SAME as database sessions! (`session != db.session`)
            session["user_id"] = new_user.id

            return make_response(new_user.to_dict(only=("id", "username", "created_at")), 201)
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)
    
# POST route to authenticate user in database using session-stored credentials.
@app.route("/login", methods=["POST"])
def user_login():
    if request.method == "POST":
        # Retrieve POST request as JSONified payload.
        payload = request.get_json()
        print(payload)

        # Filter database by username to find matching user to potentially login.
        matching_user = User.query.filter(User.username.like(f"%{payload['username']}%")).first()
        print(matching_user)

        # Check submitted password against hashed password in database for authentication.
        if matching_user is not None:
            AUTHENTICATION_IS_SUCCESSFUL = bcrypt.checkpw(
                password=payload["password"].encode("utf-8"),
                hashed_password=matching_user.password.encode("utf-8")
            )

            if AUTHENTICATION_IS_SUCCESSFUL:
                # Save authenticated user ID to server-persistent session storage.
                # NOTE: Sessions are to servers what cookies are to clients.
                # NOTE: Server sessions are NOT THE SAME as database sessions! (`session != db.session`)
                session["user_id"] = matching_user.id

                return make_response(matching_user.to_dict(only=("id", "username", "created_at")), 200)
            else:
                return make_response({"error": "Invalid username or password. Try again."}, 401)
        else:
            return make_response({"error": "Invalid username or password. Try again."}, 401)
    else:
        return make_response({"error": f"Invalid request type. (Expected POST; received {request.method}.)"}, 400)
    
# DELETE route to remove session-stored credentials for logged user.
@app.route("/logout", methods=["DELETE"])
def user_logout():
    if request.method == "DELETE":
        # Clear user ID from server-persistent session storage.
        # NOTE: Sessions are to servers what cookies are to clients.
        # NOTE: Server sessions are NOT THE SAME as database sessions! (`session != db.session`)
        session["user_id"] = None

        return make_response({"msg": "User successfully logged out."}, 204)
    else:
        return make_response({"error": f"Invalid request type. (Expected DELETE; received {request.method}.)"}, 400)


#######################################################
################ GLOBAL ERROR HANDLING ################
#######################################################


# General GET route for 404 error handling.
@app.errorhandler(404)
def page_not_found(error):
    return make_response({"error": "Page not found."}, 404)


#######################################################
######### FLASK BOILERPLATE FOR EXECUTION #############
#######################################################
        
        
if __name__ == "__main__":
    app.run()