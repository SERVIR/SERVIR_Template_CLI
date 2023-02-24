# SERVIR App Template Installer

[![Python: 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SERVIR: Global](https://img.shields.io/badge/SERVIR-Global-green)](https://servirglobal.net)

This installer will help you get the SERVIR app template installed quickly and ready to modify.

## Installation
### Create a conda environment for the installer
```shell
conda create -n app-template python=3.9
```
### Activate environment
```shell
conda activate app-template
```
### Install servir_template_cli
```shell
pip install servir-template-cli
```
cd to a directory where you would like to start the application.  I recommend this be a common development directory. 
You will create the specific directory with your project name in the next few steps. My directory where I start all 
of my web apps is named websites.  
```shell
cd path/to/your/websites/directory
```
Install the app template using servir_template create command and passing -n with the name you 
would like for your application.  This will create the directories, files, and the new conda environment
for the application.  It will take several minutes to complete creating the conda environment and give little 
information when Solving environment step is happening.  When this step is done it will continue automatically
and install all packages that you need, as well as apply all database setup actions.
```shell
servir_template create -n name_ur_app_here
```

Your application has now been created inside the directory of the name you provided above.  Enter the directory
to continue.

Before editing the application you will need to have an Earth Engine (EE) account, and a Google cloud project where 
you will enable both EE and Google Authentication.  To do that follow these steps:
1) If you do not currently have an EE account sign up https://earthengine.google.com/signup
2) Next you will need to create a google cloud project where you will enable EE and Google Authentication for your project. Navigate to https://console.cloud.google.com/projectcreate
3) Follow the prompts to create the project, you may want to name it Your_Project_Name so you can skip this part when you set up your application.
4) After you create the project you must select it from the dropdown in the top
5) In the left panel under APIs & Services click the "OAuth consent screen" link, then fill out the form with the information for your application. There are a few pages with choices, proceed when finished.
6) In the left panel click "Credentials" link
7) At the top left click + Create Credentials and select "OAuth 2.0 Client ID"
8) In the dropdown select "Web Application" and give a name.
9) In the App Domain fields use the the dev domains for example:
   1) http://127.0.0.1:8000/
   2) http://127.0.0.1:8000/terms-privacy
   3) http://127.0.0.1:8000/terms-privacy
10) Add Authorized JavaScript origins (you may enable multiple)
    1) Examples:
       1) http://localhost:8000
       2) http://127.0.0.1:8000
       3) https://your_domain
11) Add Authorized redirect URIs (you may enable multiple)
    1) Examples:
       1) http://localhost:8000/accounts/google/login/callback/
       2) http://127.0.0.1:8000/accounts/google/login/callback/
       3) https://your_domain/accounts/google/login/callback/
12) Copy and save the Client ID and Client secret to your local machine (you will need these later)
13) Click DOWNLOAD JSON and save
14) Click save
15) Click Enabled APIs & Services then click the + Enable APIS AND SERVICES link at the top
16) Search for Earth Engine, click it, then click enable.
17) Click Create Credentials again and select service account
18) Fill out information and click CREATE AND CONTINUE.
19) Click Select a role and scroll to Earth Engine, then select Earth Engine Resource Viewer
20) Register the service account https://signup.earthengine.google.com/#!/service\_accounts

That was the hard part, everything else is easy to get you up and running.  Back to your files, you should be in 
the project directory, if not, navigate there to edit the data.json file.

### Edit data.json
This file contains private information that you do not want to share with the world.  It is ignored in the .gitignore
so when you push your application to github it will not go with the rest of your files.  It is a json structure that 
looks like the following.
```json
{
  "SECRET_KEY": "{yx+Z9or:Yuisk>:&R%-NZ%oUk@BB!XAL#?RZay=^U>MDY?Qj=e^-YT3u^dp):~|",
  "ALLOWED_HOSTS": ["localhost", "127.0.0.1"],
  "CSRF_TRUSTED_ORIGINS": ["http://localhost:8000", "http://127.0.0.1:8000"],
  "private_key_json" : "path_to_key_file_from_google_console",
  "DATA_DIR" : "path_to_data_directory",
  "service_account" : "registered_ee_service_account_associated_with_key",
  "sample_netCDF": "https://thredds.servirglobal.net/thredds/fileServer/mk_aqx/geos/20191123.nc"
}
```
To begin you will need to enter the path to your key file that you created in the Google console, where it says
path_to_key_file_from_google_console.  If you are using a Windows machine be sure to use double slashes.

For DATA_DIR, create a separate directory some place, usually out of the actual application directory to store 
data.  Replace path_to_data_directory with that path.  To use the example in the template you will need to create a 
subdirectory named geos, and download
https://thredds.servirglobal.net/thredds/fileServer/mk%5C_aqx/geos/20191123.nc to the directory. 

Replace registered_ee_service_account_associated_with_key with the email address of the Google service account.

Save the data.json file

### Activate your applications conda environment
```shell
conda activate name_ur_app_here
```

### create superuser
run the following command and follow the prompts
```shell
python manage.py createsuperuser
```

## Start the App
```shell
python manage.py runserver
```

1) Open a browser and navigate to http://127.0.0.1:8000/admin/ 
2) Click Social applications
3) Click ADD SOCIAL APPLICATION
4) Select Google in the provider
5) Enter your application name in name
6) Enter the Client id from the Google console
7) Enter the Secret Key from the Google console
8) Leave Key empty
9) Select 127.0.0.1 and hit the arrow to move it to Chosen sites
10) Click Save and continue editing
11) If 127.0.0.1 is not still in Chosen sites repeat step 9 and 10. 
12) Click VIEW SITE at the top right of the screen

At this point all examples should work.


