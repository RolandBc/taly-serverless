# DEPLOY
```
cd mon_env_lambda/lib/python3.8/site-packages
cd update-jow
zip -r9 ../update-jow.zip .
```

```
aws lambda update-function-code --function-name update-jow --zip-file fileb://update-jow.zip
```

full update
```
cd update-jow && zip -r9 ../update-jow.zip . && cd .. && aws lambda update-function-code --function-name update-jow --zip-file fileb://update-jow.zip

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

