# To deploy:
pdm export -o requirements.txt

sls deploy

 # To run sls offline:
SLS_DEBUG=* sls offline start