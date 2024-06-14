import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_app.models import pet

class Person:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']  
        self.email_is_confirm = data['email_is_confirm']            
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pets = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def validate_user(data):
        is_valid = True 
   
        if len(data["email"]) == 0:
            flash("* Email cannot be empty", "email")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("* Invalid email format. Should meet username@emaildomain.com", "email")
            is_valid = False  
        if is_valid:
            flash("* Registration was successful", "first_name")
        return is_valid