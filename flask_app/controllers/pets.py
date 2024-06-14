from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.pet import Pet
from flask_app.models.user import User
import requests, os, re
from bs4 import BeautifulSoup as bs

# Updated regular expression to match US zip code, or 'City, ST' format
CITY_REGEX = re.compile(r"^(?:\d{5}|[A-Za-z ]{3,}, [A-Za-z]{2})$")

base = os.path.dirname(os.path.abspath(__file__))

@app.route("/new/application")
def create_application():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("application.html")

@app.route("/create", methods=['POST'])
def add_new_re():
    if 'user_id' not in session:
        return redirect('/')
   
    if Pet.getOnebyname(request.form["name"]) != False:
        flash("Pet is already adopted, pick another one!", "name")
        return redirect("/new/application")
    
    data = {
        "name": request.form["name"],
        "breed": request.form["breed"],
        "age": request.form["age"],
        "gender": request.form["gender"],
        "weight": request.form["weight"],
        "description": request.form["description"],
        "adopter_old_enough": request.form["adopter_old_enough"],
        "adopter_stable_income": request.form["adopter_stable_income"],
        "user_id": session["user_id"]
    }  
 
    if not Pet.validate_pet(data):
        return redirect("/new/application")
   
    Pet.create(data)
    session["name"] = request.form["name"]
    return redirect('/account')

@app.route("/pet/<int:pet_id>")
def view_instruct(pet_id):
    try:
        pet = Pet.getOneById(pet_id)
        user = User.getOneById(pet.user_id)
    except Exception as e:
        flash("Error retrieving pet or user information.", "error")
        return redirect('/account')
    return render_template("view_application.html", pet=pet, user=user)

@app.route("/pet/<int:pet_id>/edit")
def edit_pet(pet_id):
    if 'user_id' not in session:
        return redirect('/')
    
    try:
        pet = Pet.getOneById(pet_id)
        user = User.getOneById(pet.user_id)
    except Exception as e:
        flash("Error retrieving pet or user information.", "error")
        return redirect('/account')
    
    return render_template("edit_app.html", pet=pet, user=user)

@app.route("/edit/<int:pet_id>", methods=["POST"])
def update_one(pet_id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id": pet_id,
        "name": request.form["name"],
        "breed": request.form["breed"],
        "age": request.form["age"],
        "gender": request.form["gender"],
        "weight": request.form["weight"],
        "description": request.form["description"],
        "adopter_old_enough": request.form["adopter_old_enough"],
        "adopter_stable_income": request.form["adopter_stable_income"],
        "user_id": session["user_id"]
    }
   
    if not Pet.validate_pet(data):
        return redirect(f"/pet/{pet_id}/edit")
    
    try:
        Pet.edit(data)
    except Exception as e:
        flash("Error updating pet information.", "error")
        return redirect(f"/pet/{pet_id}/edit")
    
    return redirect('/account')

@app.route("/pet/<int:pet_id>/delete")
def delete_one(pet_id):
    if 'user_id' not in session:
        return redirect('/')
    
    try:
        Pet.delete(pet_id)
    except Exception as e:
        flash("Error deleting pet.", "error")
        return redirect('/account')
    
    return redirect('/account')

@app.route("/william")
def william():
    return render_template("william.html")

@app.route("/gilbert")
def gilbert(): 
    return render_template("gilbert.html")

@app.route("/beatrice")
def beatrice(): 
    return render_template("Beatrice.html")

@app.route("/shadow")
def shadow():
    return render_template("Shadow.html")

@app.route("/zoey")
def zoey():
    return render_template("Zoey.html")

@app.route("/azalea")
def azalea():
    return render_template("Piggy.html")

@app.route("/fry")
def fry():
    return render_template("Fry.html")

@app.route("/gucci")
def gucci():
    return render_template("Gucci.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/input_search")
def search():
    session["valid"] = False
    return render_template("api_pets.html")

@app.route("/search", methods=['POST'])
def input():
    session["valid"] = True

    if not CITY_REGEX.match(request.form["location"]):
        flash("* Please enter US zip code, or 'City, ST'")
        session["valid"] = False
        return redirect("/input_search")
    
    if request.form["animal"] == "":
        flash("* Please choose an animal", "animal")
        session["valid"] = False
        return redirect("/input_search")
    
    session["valid"] = True
    session["animal"] = request.form["animal"]
    session["location"] = request.form["location"]
    return redirect("/api")

@app.route("/api")
def api():
    endpoint = "https://api-staging.adoptapet.com/search/pet_search"
    params = {
        "key": "hg4nsv85lppeoqqixy3tnlt3k8lj6o0c",
        "v": "3",
        "output": "json",
        "geo_range": 50,
        "species": session.get("animal"),
        "city_or_zip": session.get("location"),
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        pets = response.json().get("pets", [])
        
    except requests.exceptions.RequestException as e:
        flash("Error connecting to pet search API.", "error")
        return redirect('/input_search')
    except ValueError as e:
        flash("Error processing API response.", "error")
        return redirect('/input_search')

    names, pics, urls, ages, genders, breeds, sizes = [], [], [], [], [], [], []
    for pet in pets:
        pet_id = pet.get('pet_id')
        names.append(pet.get("pet_name"))
        pics.append(pet.get("large_results_photo_url"))
        urls.append(f"https://www-staging.adoptapet.com/pet/{pet_id}")
        ages.append(pet.get("age"))
        genders.append(pet.get("sex"))
        breeds.append(pet.get("primary_breed"))
        sizes.append(pet.get("size"))

    session.pop("animal")
    session.pop("location")
    return render_template("api_pets.html", names=names, pics=pics, urls=urls, ages=ages, genders=genders, breeds=breeds, sizes=sizes)