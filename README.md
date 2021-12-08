# MusicAI - melody generation web app

[MusicAI](https://github.com/Exital/musicAI) is a melody generation web app project showing the work of our
AI final project [236502](https://github.com/LiorSherman/236502).

## Prerequisites

> __Below we assume the working directory is the repository root.__

### Install dependencies

> __optional__ - create .env file at the repo's root and export DEBUG settings.
> 
> If no .env file is found - DEBUG will be assigned with default value of TRUE
   ```sh
  # export environment variables, for local server use DEBUG=TRUE
  export DEBUG=True
  ```
- Create your virtual environment
- Install the dependencies using pip

  ```sh
  # Install the dependencies
  pip install -r requirements.txt
  ```
  
### Running on local server

> After installing the requirements, make sure your environment is activated and use the following command from the repo's root folder.

```sh
$ python manage.py runserver
```
You will receive a link to access your local server
```sh
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 08, 2021 - 20:59:27
Django version 3.2.5, using settings 'rocket_webapp.settings'
Starting development server at http://127.0.0.1:8000
Quit the server with CONTROL-C.
```
