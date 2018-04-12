from wtforms import Form, StringField, IntegerField, SelectField, PasswordField, validators, widgets
import re


class SignUpForm(Form):
    email = StringField('Adresse courriel', [validators.Email(message="Cette adresse email est invalide"),
                                             validators.Length(max=100, message="Cette adresse email est trop longue")])

    # ADD REGEX FOR PASSWORD
    password = PasswordField('Mot de passe',
                             [validators.EqualTo('passwordConfirm', message='les mots de passes doivent correspondre'), validators.regexp(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", message='Le mot de passe doit contenir au moins 8 caracteres, 1 chiffre et une lettre')])

    passwordConfirm = PasswordField('Confirmer le mot de passe')


class LoginForm(Form):
    email = StringField('Adresse courriel', [validators.data_required(message='Ce champ doit etre remplis')])
    password = PasswordField('Mot de passe', [validators.data_required(message='Ce champ doit etre remplis')])


class PriceForm(Form):
    minPrice = IntegerField('Prix minimum', [validators.optional(), validators.number_range(min=0, message='le montant doit etre positif')], widget=widgets.Input(input_type="number"))
    maxPrice = IntegerField('Prix maximum', [validators.optional(), validators.number_range(min=0, message='le montant doit etre positif')], widget=widgets.Input(input_type="number"))
    priceOrder = SelectField('Ordre de tri des prix', choices=[('ASC', 'Croissant'), ('DESC', 'Decroissant')])