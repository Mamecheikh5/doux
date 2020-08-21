from flask import flash, redirect, render_template, url_for,jsonify,Response,request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_microservice 
from .forms import LoginForm, RegistrationForm
import urllib.request
from .. import db
from ..models import utilisateur
import requests
from requests import post
import json
from json import JSONEncoder


REGISTER_USER_URL = 'http://127.0.0.1:5007/api/register/'
LOGIN_USER_URL = 'http://127.0.0.1:5007/api/login/'



@auth_microservice.route('/register.html', methods=['GET','POST'])
def register():
    
    form = RegistrationForm()
    if form.validate_on_submit():
        
    

    
        Utilisateur = utilisateur(email=form.email.data,
                                username=form.username.data,
                                nom=form.nom.data,
                                prenom=form.prenom.data,
                                password=form.password.data)
        json_reg={
                "email": Utilisateur.email,
                "username": Utilisateur.username,
                "nom": Utilisateur.nom,
                "prenom": Utilisateur.prenom,
                "password": form.password.data
                }

        response = jsonify(json_reg)
        r = response.json
        flash('You have successfully registered! You may now login.')
        r = requests.post(url=REGISTER_USER_URL, json=r)
        
        return redirect(url_for('auth_microservice.login'))
    return render_template('auth/register.html', form=form, title='Register')



@auth_microservice.route('/login.html', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # renvoyer 

        json_em={
                "email": form.email.data,
                "password": form.password.data
                }
        response = jsonify(json_em)
        r = response.json

        reponse = requests.post(url=LOGIN_USER_URL, json=r)
        # Verification de l'existence de l'utilsateur dans notre BDD
        # si le mdp correspond dans la bdd
        
        reponse = reponse.json()

        if reponse !='Invalid email or password.': #is not None and r.verify_password(
               # form.password.data):
            # connexion de l'utilisateur
            user = utilisateur(email=reponse['email'],
                                username=reponse['username'],
                                nom=reponse['nom'],
                                prenom=reponse['prenom']
                                )#password=password)
            login_user(user)

            # redirection au  menu  apres la connexion
            return redirect(url_for('home.dashboard'))
        else:
            # Au cas ou les informations sont incorects
            
            flash('Invalid email or password.')

    # chargement de la template de connexion
    return render_template('auth/login.html', form=form, title='Login')


@auth_microservice.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Deconnecter un utilisateur avec le lien logout
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirection à la page de connexion
    return redirect(url_for('auth_microservice.login'))
    