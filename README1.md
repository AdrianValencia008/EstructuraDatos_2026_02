# Estructuras de Datos y Algoritmos en Python (alternativa con Google Colab)

Este curso está diseñado para trabajar con **GitHub Codespaces** (ver `README.md`). Si la
conexión de tu universidad **bloquea Codespaces**, puedes seguir el curso igual usando
**Google Colab** para clonar tu fork, trabajar y guardar tu progreso en GitHub.

---

# 🍴 Paso obligatorio: hacer un Fork

Antes de comenzar:

1. Entra a https://github.com/arleyfernandotorresgalindo/EstructuraDatos_2026_02
2. Haz clic en el botón **Fork** (arriba a la derecha en GitHub)
3. Se creará una copia del repositorio en **tu cuenta personal**

👉 A partir de ahora trabajarás en **tu propio repositorio** (tu fork).

---

# 🔑 Crear un Personal Access Token (PAT)

Colab no puede iniciar sesión en GitHub con usuario/contraseña, así que necesitas un token:

1. En GitHub: foto de perfil → **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens**
2. **Generate new token**
3. Limita el token a tu repositorio (el fork)
4. Dale permiso de **Contents: Read and write**
5. Genera y copia el token (solo se muestra una vez — guárdalo en un lugar seguro)

## Guardarlo en Colab Secrets (recomendado)

1. En Colab, click en el ícono de llave 🔑 en la barra lateral izquierda
2. **Add new secret** → nombre `GITHUB_TOKEN` → pega el valor del token
3. Activa el switch **"Notebook access"**

Así no tienes que volver a pegar el token cada vez.

---

# 🚀 Cómo empezar

## 1. Clonar tu fork (una sola vez)

Abre un notebook nuevo en Colab y ejecuta:

```python
from google.colab import drive
drive.mount('/content/drive')

from google.colab import userdata
token = userdata.get('GITHUB_TOKEN')
username = "tu-usuario-de-github"
repo = "EstructuraDatos_2026_02"

%cd "/content/drive/MyDrive/Colab Notebooks"
!git clone --recurse-submodules https://{username}:{token}@github.com/{username}/{repo}.git
%cd {repo}
!git config user.email "tu_correo@example.com"
!git config user.name "Tu Nombre"
!git config merge.ours.driver true
!git remote add upstream https://{username}:{token}@github.com/arleyfernandotorresgalindo/EstructuraDatos_2026_02.git
```

> La primera vez que ejecutes esto, Colab te pedirá autorizar el acceso al secreto (aparece un
> aviso arriba del notebook) — dale **"Grant access"**.

Esto deja el repositorio guardado en tu Google Drive, en
`MyDrive/Colab Notebooks/EstructuraDatos_2026_02`, así que **solo necesitas clonarlo una vez**.

- El flag `--recurse-submodules` es necesario para que la carpeta `goodrich/` (que es un
  submódulo de git) se descargue con contenido y no quede vacía.
- `git config merge.ours.driver true` evita conflictos cuando el profesor actualiza los
  notebooks del curso.
- `git remote add upstream ...` conecta tu fork con el repositorio del profesor, para poder
  traer contenido nuevo más adelante (sección "Actualizar el contenido del curso"). Se usa tu
  token también aquí (aunque el repo del profesor es público) para evitar el error
  `fatal: could not read Username for 'https://github.com'`, que ocurre porque Colab no tiene
  una terminal interactiva para pedir credenciales.

Estos tres `git config`/`remote add` se ejecutan **una sola vez**: quedan guardados en
`.git/config` dentro de la carpeta clonada (que vive en tu Drive), así que no se repiten en
clases futuras.

## 2. Entrar al repositorio cada clase

En las siguientes clases **no vuelvas a clonar** — solo monta Drive y entra a la carpeta:

```python
from google.colab import drive
drive.mount('/content/drive')

%cd "/content/drive/MyDrive/Colab Notebooks/EstructuraDatos_2026_02"
```

---

# 📁 Estructura del repositorio

```
.
├── goodrich/        # Código fuente del libro (NO modificar)
├── notebooks/       # Notebooks de clase con teoría (NO modificar)
└── student_work/    # ← TU TRABAJO VA AQUÍ
```

---

# ⚠️ Reglas importantes

🔴 **NO modifiques:**

- `goodrich/`
- `notebooks/`

🟢 **Trabaja únicamente en:**

```
student_work/
```

El profesor **nunca** modifica esa carpeta. Tu trabajo ahí está siempre seguro.

---

# 🔄 Actualizar el contenido del curso

Cuando el profesor publique material nuevo, debes traer esos cambios a tu fork. El remoto
`upstream` ya quedó conectado desde el clonado inicial (sección "Cómo empezar"), así que solo
necesitas ejecutar esto dentro de la carpeta del repositorio:

```python
!git fetch upstream              # Trae lo del profe
!git rebase upstream/main        # Te pones al día
!git submodule update            # Actualiza el código del libro (goodrich/)
!git push origin main --force    # Subes tu versión actualizada
```

👆 Esto actualiza tu fork con el material nuevo sin perder tu trabajo en `student_work/`

---

# 💾 Guardar tu trabajo

```python
!git add student_work/
!git commit -m "descripción de lo que hice"
!git push
```

Se recomienda hacer `push` varias veces durante la clase, no solo al final, para no perder
trabajo si la sesión de Colab se desconecta.

---

# 📓 Uso de Jupyter (notebooks) en Colab

1. En Colab, click en el ícono de **carpeta** 📁 en la barra lateral izquierda (panel de archivos)
2. Navega hasta `drive/MyDrive/Colab Notebooks/EstructuraDatos_2026_02/notebooks/`
3. **Doble click** sobre el archivo `.ipynb` para abrirlo

> No uses **File → Open notebook → GitHub** para esto: esa opción abre una copia aislada que no
> está conectada a la carpeta clonada, y no podrías guardar tus cambios con `git push`.

---

# 🔁 Flujo de trabajo recomendado

1. Monta Drive y entra a la carpeta del repositorio (paso 2 de "Cómo empezar")
2. Actualiza el contenido del curso (sección "Actualizar el contenido del curso")
3. Revisa la teoría en `notebooks/`
4. Resuelve y guarda tu trabajo en `student_work/`
5. Haz `git add`, `commit` y `push` antes de terminar la clase

---

# ❓ Problemas comunes

### No aparecen cambios del profesor

```python
!git fetch upstream
!git rebase upstream/main
!git submodule update
!git push origin main --force
```

### Error al hacer rebase (cambios locales sin guardar)

```python
!git stash
!git rebase upstream/main
!git stash pop
!git push origin main --force
```

### `fatal: could not read Username for 'https://github.com'`

El remoto `upstream` (o `origin`) no tiene credenciales y Colab no puede pedirlas de forma
interactiva. Agrega el token a la URL del remoto (ver sección "Actualizar el contenido del curso").

### La carpeta `goodrich/` aparece vacía

Faltó el flag `--recurse-submodules` al clonar. Sin volver a clonar todo, ejecuta dentro de la
carpeta del repositorio:

```python
!git submodule update --init --recursive
```

### Quiero descartar cambios locales sin guardar

```python
!git checkout -- .        # descarta cambios en archivos ya rastreados por git
!git clean -fd            # borra archivos/carpetas nuevos que no están rastreados
```

⚠️ Esto es **irreversible**. Si tienes trabajo sin guardar que sí quieres conservar, primero
haz `commit` (o `git stash`) antes de descartar nada.

### Mi red universitaria también bloquea github.com

Si tu red bloquea el acceso a `github.com` por completo (no solo a Codespaces), este método
tampoco funcionará. Verifica primero que puedas clonar el repositorio desde esa red.

---

## 👨‍🏫 Autor

Curso diseñado por **Arley Fernando Torres Galindo**.
