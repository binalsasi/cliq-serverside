# cliq

  Cliq is a photo sharing platform made using Flutter and Django (as the server)
  
## Getting Started

1. install django, PIL (or pillow), mysql (mariadb).
2. edit cliq/cliq/settings.py
    - add security key
    - add database configurations
3. run server.

Note : if running it locally, change the read, write, generateThumbnail, saveImage, getThumbnail, getImage functions
  in cliq/Functions.py, use the -x suffixed counterparts within the same file.

if hosting it in Google App Engine:
read this : https://medium.com/@BennettGarner/deploying-a-django-application-to-google-app-engine-f9c91a30bd35
