from app.models import CustomUser, Post
from rest_framework_simplejwt.tokens import RefreshToken
import pickle

tokens = []

for user in CustomUser.objects.all():
    token = RefreshToken.for_user(user)
    string = str(token.access_token)
    tokens.append(string)

with open("token.dump", "wb") as f:
    pickle.dump(tokens, f)