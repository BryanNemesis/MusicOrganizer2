# To deploy:
pdm export -o requirements.txt

sls deploy

 # To run sls offline:
SLS_DEBUG=* sls offline start

# Remarks
Im thinking in the app there's gonna be a login prompt right away if user_id cookie is not present and then all endpoints can operate with assumption that it exists.
Probably there's going to be an endpoint for login and we can remove authorize from get_saved_albums and also use only the user client.
