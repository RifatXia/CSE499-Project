from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Replace 'rifatxia' with the username of the user you want to generate a token for
user = User.objects.get(username='rifatxia')
token, created = Token.objects.get_or_create(user=user)