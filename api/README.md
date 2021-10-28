# To deploy:
pdm export -o requirements.txt

sls deploy

 # To run sls offline:
SLS_DEBUG=* sls offline start

# Remarks
Im thinking in the app there's gonna be a login prompt right away if user_id cookie is not present and then all endpoints can operate with assumption that it exists.
Probably there's going to be an endpoint for login and we can remove authorize from get_saved_albums and also use only the user client.

ok so login endpoint should save a cookie and tokens into the db if they're not there, and otherwise just return some data that login is not needed.
all the other endpoints will work only when logged in. there should be a method in all the other endpoints to get the token to use with spotify client which would also refresh the token if needed.

login endpoint:
if user_id cookie not present and user not in db - return a url to redirect to login.
else - 