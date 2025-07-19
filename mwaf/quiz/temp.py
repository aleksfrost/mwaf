from models import Users
from django.contrib.auth.hashers import make_password


for_user = make_password("40летЧелябинска")
user = Users(username='Elena', password=for_user, is_admin=True)
user.save()