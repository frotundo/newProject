# from django.db.models import Q


# Book.objects.filter((
#     Q(title__startswith='A-') | 
#     Q(title__startswith='MPS-') | 
#     Q(title__startswith='S-')) & 
#     Q(title__regex=r'^.*-{2}.*$'))


"""Para enviar un correo electrónico informativo en Django cuando se ejecuta una función, puedes utilizar la función de correo incorporada de Django, llamada send_mail. Esta función se encuentra en el módulo django.core.mail y te permite enviar correos electrónicos utilizando la configuración de correo de tu aplicación.}

Ejemplo:"""
# from django.core.mail import send_mail

# def my_function():
#     # Your function code here
#     ...
#     send_mail(
#         'Subject here',
#         'Here is the message.',
#         'from@example.com',
#         ['to@example.com'],
#         fail_silently=False,
#     )

"""En este ejemplo, la función send_mail se utiliza para enviar un correo electrónico con el asunto "Subject here" y el cuerpo del mensaje "Here is the message." desde "from@example.com" hacia "to@example.com". El parámetro fail_silently se utiliza para especificar si se debe o no mostrar una excepción en caso de error al enviar el correo electrónico.

Es importante mencionar que para usar esta función es necesario configurar correctamente el servidor de correo en tu proyecto de Django, para esto debes configurar el archivo settings.py de tu proyecto con la información del servidor de correo que deseas usar."""
# ----------------------------------------------------------------
"""Existen varias opciones para desplegar un proyecto de Django en un servidor, algunas de las opciones más populares son:

Utilizando un servidor web como Apache o Nginx con mod_wsgi. Esta es una de las opciones más comunes y soportadas por muchos proveedores de alojamiento web. Puedes seguir un tutorial como este para configurar tu proyecto en un servidor Apache con mod_wsgi: https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/modwsgi/

Utilizando un contenedor de Docker. Puedes crear una imagen de Docker con tu proyecto de Django y desplegarlo en un servidor con Docker. Un tutorial para hacer esto se puede encontrar aquí: https://runnable.com/docker/python/dockerize-your-python-application

Utilizando un servicio de plataforma como Heroku. Heroku es una plataforma en la nube que te permite desplegar fácilmente tu proyecto de Django sin tener que preocuparte por la configuración del servidor. Puedes seguir un tutorial como este para desplegar tu proyecto en Heroku: https://devcenter.heroku.com/articles/getting-started-with-python

Utilizando un proveedor de servicios de computación en la nube como AWS, Google Cloud o Azure. Cada uno de estos proveedores ofrece opciones para desplegar una aplicación Django en un servidor virtual o en un contenedor.

En resumen, hay varias opciones para desplegar un proyecto de Django, pero las opciones más populares son utilizar un servidor web con mod_wsgi, utilizar contenedores de Docker y utilizar un servicio de plataforma como Heroku o un proveedor de computación en la nube como AWS, Google Cloud o Azure.

La configuración de Nginx con mod_wsgi para servir una aplicación Django consta de varios pasos:

1. Instalar Nginx y mod_wsgi en el servidor. Puedes hacerlo utilizando el administrador de paquetes de tu sistema operativo (apt-get en Ubuntu, yum en CentOS, etc.)

2. Crear un archivo de configuración para tu aplicación Django en la ruta de configuración de Nginx (normalmente /etc/nginx/sites-available/). El archivo debe tener algo similar a esto:

server {
    listen 80;
    server_name example.com;
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/static/;
    }
}

3. En este archivo se esta configurando el proxy para que apunte a una direccion localhost:8000 que es donde se ejecutara el servidor mod_wsgi, y tambien se esta indicando la ruta de los archivos estaticos

4. Crear un archivo wsgi.py en la raíz de tu proyecto Django con el siguiente contenido:

import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

application = Cling(get_wsgi_application())

5. En este archivo se esta importando los modulos necesarios para ejecutar el servidor mod_wsgi y se esta indicando el archivo de configuracion de django.

6. Ejecutar el servidor mod_wsgi utilizando el archivo wsgi.py creado anteriormente. Puedes hacerlo utilizando un archivo de inicio similar a este:

#!/bin/bash

source /path/to/virtualenv/bin/activate
export DJANGO_SETTINGS_MODULE=myproject.settings
exec /usr/local/bin/gunicorn myproject.wsgi:application --bind=127.0.0.1:8000

7. Finalmente, enlaza el archivo de configuración de Nginx con el archivo de configuración de sites-enabled y reinicia Nginx.

sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled/
sudo service nginx restart

Ten en cuenta que esta es solo una configuración básica y puede variar según tus necesidades específicas. También es importante asegurarte de que tienes permisos adecuados para acceder a los archivos y carpetas necesarios, y que los archivos de configuración estén correctamente escritos. Además, es recomendable monitorear los registros de Nginx y mod_wsgi para detectar y solucionar problemas.
"""

"""La configuración de Apache con mod_wsgi para servir una aplicación Django consta de varios pasos:

1. Instalar Apache y mod_wsgi en el servidor. Puedes hacerlo utilizando el administrador de paquetes de tu sistema operativo (apt-get en Ubuntu, yum en CentOS, etc.)

2. Crear un archivo de configuración para tu aplicación Django en la ruta de configuración de Apache (normalmente /etc/httpd/conf.d/ o /etc/apache2/sites-available/)

3. El archivo debe tener algo similar a esto:

WSGIScriptAlias / /path/to/your/project/wsgi.py
WSGIPythonPath /path/to/your/project

<Directory /path/to/your/project>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

4. En este archivo se esta configurando el Alias para que apunte a una direccion /path/to/your/project/wsgi.py que es donde se ejecutara el servidor mod_wsgi, y tambien se esta indicando la ruta del proyecto

5. Crear un archivo wsgi.py en la raíz de tu proyecto Django con el siguiente contenido:

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

application = get_wsgi_application()

6. En este archivo se esta importando los modulos necesarios para ejecutar el servidor mod_wsgi y se esta indicando el archivo de configuracion de django.

7. Habilitar el módulo mod_wsgi en Apache y reinicie el servidor.

sudo a2enmod wsgi
sudo service apache2 restart

Ten en cuenta que esta es solo una configuración básica y puede variar según tus necesidades específicas. También es importante asegurarte de que tienes permisos adecuados para acceder a los archivos y carpetas necesarios, y que los archivos de configuración estén correctamente escritos. Además, es recomendable monitorear los registros de Apache y mod_wsgi para detectar y solucionar problemas."""


    # user = request.user
    # groups = user.groups.all()
    # print(groups)
print('Hola mundo')

from math import ceil

print(ceil(9.9))
print(ceil(1.1))