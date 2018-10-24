from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, form):
        errors = {}

        # validate first name
        if len(form['first_name']) < 2 or not form['first_name'].isalpha():
            if len(form['first_name']) < 2:
                errors['first_name_length'] = "First name must be at least 2 characters."
            if not form['first_name'].isalpha():
                errors['first_name_alpha'] = "First name can only contain letters."

        # validate last name
        if len(form['last_name']) < 2 or not form['last_name'].isalpha():
            if len(form['last_name']) < 2:
                errors['last_name_length'] = "Last name must be at least 2 characters."
            if not form['last_name'].isalpha():
                errors['last_name_alpha'] = "Last name can only contain letters."

        # validate email
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Invalid email address."
        try:
            self.get(email=form['email'])
            errors['email'] = "Email is already in use."
        except:
            pass

        # validate password
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        
        if form['password'] != form['confirm_pw']:
            errors['confirm_pw'] = "Password do not match."

        return errors

    def create_user(self, user_data):
        pw_hash = bcrypt.hashpw(user_data['password'].encode(), bcrypt.gensalt())
        user = self.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=pw_hash
        )
        return user

    def login(self, form):
        # find the user with the given email
        user = self.filter(email=form['email'])
        if len(user) > 0:
            # email found
            if bcrypt.checkpw(form['password'].encode(), user[0].password.encode()):
                # email and password match
                return(True, user[0].id)
            else:
                # password does not match
                return(False, "Incorrect email/password combination.")
        else:
            # email not found
            return(False, "Account does not exist.")

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name="user_comments")
    message = models.ForeignKey(Message, related_name="message_comments") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)