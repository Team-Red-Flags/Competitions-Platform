[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/MadMoose02/Competitions-Platform)
<a href="https://render.com/deploy?repo=https://github.com/MadMoose02/Competitions-Platform">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>


# Project Overview
This is a web application to manage user submissions for coding competitions. Assignment solution by the RED FLAGS team for the COMP 3613 Software Engineering II Assignment 1. Based on the Flask MVC template found [here](https://github.com/uwidcit/flaskmvc).


# Dependencies
* Python3/pip3
* Packages listed in [requirements.txt](https://github.com/MadMoose02/Power-House-Fitness-Club/blob/master/requirements.txt)

## Installing Dependencies from Requirements File
```bash
$ pip install -r requirements.txt
```


# Running the Project
_For development run the serve command (what you execute):_
```bash
$ flask run
```
_For production using gunicorn (what heroku executes):_
```bash
$ gunicorn wsgi
```

# Deploying
You can deploy your version of this app to Render by clicking on the "Deploy to Render" button above.