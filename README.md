Sample test framework 2023

***
### Preparation:

#### Clone project and install requirements using
```pip install -r requirements.txt```

#### Dev requirements can be installed via
```pip install -r requirements_dev.txt```

***
### Running tests:
```python3 -m pytest tests```

#### Run tests on N threads
```python3 -m pytest tests -n 2```

#### You can pass config variables to pytest using flags:
```--stand```  
```--launch```  
```--default```  
```--keycloak_login```  
```--keycloak_password```  
```--user_login```  
```--user_password```  
```--admin_password```  


### example:
```python3 -m pytest --launch local -k 'not complex_case' --stand st_name --keycloak_password 1234 tests/file_upload```

#### Tests are separated into two categories: 
#### - Regular (```-k 'not complex_case'```)
#### - Complex (should be run only in one thread) (```-k 'complex_case'```)

***

### Additional info:

#### To run tests and generate local Allure report please use
```python3 -m pytest tests --alluredir=tests/reports```

#### Prepare local html report by running
```allure serve tests/reports```



#### 

***

#### Before commit please run linter 
```flake8 .```

#### and autoformat with
```black .```

#### Project also setup to run isort optionally
```isort .```