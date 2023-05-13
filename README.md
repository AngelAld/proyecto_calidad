# Proyecto de Calidad de Software

## Instalación

```bash
git clone https://github.com/AngelAld/proyecto_calidad.git #clona el repo

cd proyecto_calidad # entras a la carpeta del repo

git branch 'nombre de su rama' # crea el nombre de tu rama

git checkout 'nombre de su rama' # cambias a tu rama

py -3 -m venv .venv # crea el entorno virtual de python (importante, si no lo haces puedes arruinar tu python)

.venv\Scripts\activate # inicia el entorno virtual

pip install Flask psycopg2 # instala las dependencias 

```

## Uso

```bash

git checkout 'nombre de su rama' # así cambian a su rama, por si acaso

git add . # para añadir los cambios

git commit -m "lo que quieran comentar" # para confirmar los cambios

git push -u origin 'nombre de su rama' # para enviar los cambios a su rama en el repo
```
