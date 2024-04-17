# DEPLOY
```
cd mon_env_lambda/lib/python3.8/site-packages
cd update-latournee
zip -r9 ../update-latournee.zip .
```

```
aws lambda update-function-code --function-name update-latournee --zip-file fileb://update-latournee.zip
```

full update
```
cd update-latournee && zip -r9 ../update-latournee.zip . && cd .. && aws lambda update-function-code --function-name update-latournee --zip-file fileb://update-latournee.zip

```

# LAYER (python dependencies)
```
mkdir -p dependencies/python
cd dependencies/python
```
```
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib -t .
```
```
cd ..
zip -r my_layer.zip python/
```
```
aws lambda publish-layer-version --layer-name "MyPythonLibraries" --description "Common Python libraries" --zip-file fileb://my_layer.zip --compatible-runtimes python3.8

```

