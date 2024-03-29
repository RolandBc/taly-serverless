# DEPLOY
```
cd mon_env_lambda/lib/python3.8/site-packages
cd dynamo-to-gsheet
zip -r9 ../dynamo-to-gsheet.zip .
```

```
aws lambda update-function-code --function-name dynamo-to-google-sheet --zip-file fileb://dynamo-to-gsheet.zip
```

full update
```
cd dynamo-to-gsheet && zip -r9 ../dynamo-to-gsheet.zip . && cd .. && aws lambda update-function-code --function-name dynamo-to-google-sheet --zip-file fileb://dynamo-to-gsheet.zip

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

