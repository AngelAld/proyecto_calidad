# Proyecto de Calidad de Software

## Instalación

```bash
git clone https://github.com/AngelAld/proyecto_calidad.git #clona el repo

cd proyecto_calidad # entras a la carpeta del repo

git branch nombre_de_su_rama # crea el nombre de tu rama

git checkout nombre_de_su_rama # cambias a tu rama

py -3 -m venv .venv # crea el entorno virtual de python (importante, si no lo haces puedes 
                    # arruinar tu python)

.venv\Scripts\activate # inicia el entorno virtual

pip install Flask psycopg2 # instala las dependencias 

```

## Uso

```bash

git checkout nombre_de_su_rama # así cambian a su rama, por si acaso

git add . # para añadir los cambios

git commit -m "lo que quieran comentar" # para confirmar los cambios

git push -u origin nombre_de_su_rama # para enviar los cambios a su rama en el repo
```  

### Luego de eso abren el repo en Github

```git
Esto es para poder implementar sus cambios en el proyecto principal
```

![paso1](https://hackmd.io/_uploads/HyUuFin43.png)

---
![paso2](https://hackmd.io/_uploads/SysCOin4n.png)

---
![paso3](https://hackmd.io/_uploads/BJOEYj3N3.png)

---
![paso4](https://hackmd.io/_uploads/Skqbson4h.png)

---
![paso5](https://hackmd.io/_uploads/rkgsoshV3.png)

---

### Luego de que los cambios fueran aprobados o de que alguien haya actualizado antes que ustedes

```bash
git add .
git commit -m "comentario"
git pull origin main # para descargar los cambios a tu rama
```
Probablemente aparezcan los dos cambios en su editor
Le dan a **"accept both changes"**

