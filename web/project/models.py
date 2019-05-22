from project import db, bcrypt, app
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime
from markdown import markdown
from flask import url_for
import bleach
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from project.recipes.forms import AddRecipeForm, EditRecipeForm
from werkzeug.utils import secure_filename
import os


# Allowable HTML tags
allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'p']


class ValidationError(ValueError):
    """Class for handling validation errors during
       import of recipe data via API
    """
    pass


class Recipe(db.Model):
    """Recipe fields to add:
        date last modified
    """
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    recipe_title = db.Column(db.String, nullable=True)
    recipe_description = db.Column(db.String, nullable=True)
    is_public = db.Column(db.Boolean, nullable=True)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    recipe_type = db.Column(db.String, default=None, nullable=True)
    rating = db.Column(db.Integer, default=None, nullable=True)
    ingredients = db.Column(db.Text, default=None, nullable=True)
    ingredients_html = db.Column(db.Text, default=None, nullable=True)
    recipe_steps = db.Column(db.Text, default=None, nullable=True)
    recipe_steps_html = db.Column(db.Text, default=None, nullable=True)
    inspiration = db.Column(db.String, default=None, nullable=True)
    dairy_free_recipe = db.Column(db.Boolean, nullable=True)
    soy_free_recipe = db.Column(db.Boolean, nullable=True)
    date_created = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title=None, description=None, user_id=None, is_public=False, image_filename=None, image_url=None,
                 recipe_type=None, rating=None, ingredients=None, recipe_steps=None, inspiration=None,
                 dairy_free_recipe=False, soy_free_recipe=False, date_created=None):
        self.recipe_title = title
        self.recipe_description = description
        self.is_public = is_public
        self.image_filename = image_filename
        self.image_url = image_url
        self.recipe_type = recipe_type
        self.rating = rating
        self.ingredients = ingredients
        self.recipe_steps = recipe_steps
        self.inspiration = inspiration
        self.dairy_free_recipe = dairy_free_recipe
        self.soy_free_recipe = soy_free_recipe
        self.date_created = date_created
        self.user_id = user_id

    def __repr__(self):
        print( 'BEG __repr__', flush=True )
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.recipe_title, self.user_id)

    def get_url(self):
        return url_for('recipes_api.api1_2_get_recipe', recipe_id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'title': self.recipe_title,
            'description': self.recipe_description,
            'public': self.is_public,
            'image_filename': self.image_filename,
            'image_url': self.image_url,
            'recipe_type': self.recipe_type,
            'rating': self.rating,
            'ingredients': self.ingredients,
            'recipe_steps': self.recipe_steps,
            'inspiration': self.inspiration,
            'dairy_free_recipe': self.dairy_free_recipe,
            'soy_free_recipe': self.soy_free_recipe,
            'user_id': self.user_id
        }

    def import_data(self, request):
        """Import the data for this recipe by either saving the image associated
        with this recipe or saving the metadata associated with the recipe. If
        the metadata is being processed, the title and description of the recipe
        must always be specified."""
        try:
            if 'recipe_image' in request.files:
                file = request.files['recipe_image']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['IMAGE_FOLDER'], filename))
                url = os.path.join(app.config['IMAGE_URL'], filename)
                self.image_filename = filename
                self.image_url = url
            else:
                json_data = request.get_json()
                self.recipe_title = json_data['title']
                self.recipe_description = json_data['description']
                if 'recipe_type' in json_data:
                    self.recipe_type = json_data['recipe_type']
                if 'rating' in json_data:
                    self.rating = json_data['rating']
                if 'ingredients' in json_data:
                    self.ingredients = json_data['ingredients']
                if 'recipe_steps' in json_data:
                    self.recipe_steps = json_data['recipe_steps']
                if 'inspiration' in json_data:
                    self.inspiration = json_data['inspiration']
        except KeyError as e:
            raise ValidationError('Invalid recipe: missing ' + e.args[0])
        return self

    def import_form_data(self, request, form):
        """Import the data for this recipe that was input via the EditRecipeForm
        class.  This can either be done by the user for the recipes that they own
        or by the administrator.  Additionally, it is assumed that the form has
        already been validated prior to being passed in here."""
        try:
            if form.recipe_title.data != self.recipe_title:
                self.recipe_title = form.recipe_title.data

            if form.recipe_description.data != self.recipe_description:
                self.recipe_description = form.recipe_description.data

            if form.recipe_public.data != self.is_public:
                self.is_public = form.recipe_public.data

            if form.recipe_dairy_free.data != self.dairy_free_recipe:
                self.dairy_free_recipe = form.recipe_dairy_free.data

            if form.recipe_soy_free.data != self.soy_free_recipe:
                self.soy_free_recipe = form.recipe_soy_free.data

            if form.recipe_type.data != self.recipe_type:
                self.recipe_type = form.recipe_type.data

            if form.recipe_rating.data != str(self.rating):
                self.rating = form.recipe_rating.data

            if form.recipe_image.has_file():
                file = request.files['recipe_image']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['IMAGE_FOLDER'], filename))
                url = os.path.join(app.config['IMAGE_URL'], filename)
                self.image_filename = filename
                self.image_url = url

            if form.recipe_ingredients.data != self.ingredients:
                self.ingredients = form.recipe_ingredients.data

            if form.recipe_steps.data != self.recipe_steps:
                self.recipe_steps = form.recipe_steps.data

            if form.recipe_inspiration.data != self.inspiration:
                self.inspiration = form.recipe_inspiration.data

        except KeyError as e:
            raise ValidationError('Invalid recipe: missing ' + e.args[0])
        return self

    @staticmethod
    def on_changed_ingredients(target, value, oldvalue, iterator):
        if value:
            target.ingredients_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                                  tags=allowed_tags, strip=True))

    @staticmethod
    def on_changed_recipe_steps(target, value, oldvalue, iterator):
        if value:
            target.recipe_steps_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                                   tags=allowed_tags, strip=True))

db.event.listen(Recipe.ingredients, 'set', Recipe.on_changed_ingredients)
db.event.listen(Recipe.recipe_steps, 'set', Recipe.on_changed_recipe_steps)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, default='user')
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')

    def __init__(self, email, plaintext_password, email_confirmation_sent_on=None, role='user'):
        self.email = email
        self._password = bcrypt.generate_password_hash(bytes(plaintext_password, 'utf-8'))
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
        self.role = role

    def import_form_data(self, form):
        """Import the data for this recipe that was input via the EditUserForm
        class.  This can only be done by the administrator.  Additionally, it
        is assumed that the form has already been validated prior to being
        passed in here."""
        try:
            if form.email.data != self.email:
                self.email = form.email.data

            if form.user_role.data != self.role:
                self.role = form.user_role.data

            if form.email_confirmed.data and not self.email_confirmed:
                self.email_confirmed = True
                self.email_confirmed_on = datetime.now()
            elif not form.email_confirmed.data and self.email_confirmed:
                self.email_confirmed = False
                self.email_confirmed_on = None

            if form.new_password.data:
                self._password = form.new_password.data

        except KeyError as e:
            raise ValidationError('Invalid user: missing ' + e.args[0])
        return self

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, plaintext_password):
        self.password = bcrypt.generate_password_hash(bytes(plaintext_password, 'utf-8'))

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password, bytes(plaintext_password, 'utf-8'))

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User {}>'.format(self.email)

