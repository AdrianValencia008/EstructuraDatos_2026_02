# Estructuras de Datos y Algoritmos en Python

Bienvenido al repositorio del curso de **Estructuras de Datos y Algoritmos con Python**, basado en **Goodrich, Tamassia & Goldwasser**.

El curso está diseñado para trabajar con **GitHub Codespaces**, sin necesidad de instalar nada en tu computador.

---

# 🍴 Paso obligatorio: hacer un Fork

Antes de comenzar:

1. Haz clic en el botón **Fork** (arriba a la derecha en GitHub)
2. Se creará una copia del repositorio en **tu cuenta personal**

👉 A partir de ahora trabajarás en **tu propio repositorio**

---

# 🚀 Cómo empezar

## 1. Crear tu entorno en la nube

En **tu fork**:

1. Haz clic en **Code**
2. Ve a la pestaña **Codespaces**
3. Haz clic en **Create codespace on master**

⏳ La primera vez puede tardar unos minutos.

---

## 2. Entorno listo automáticamente

El entorno incluye:

- Python 3.12
- Jupyter Notebook
- Librerías necesarias para el curso

No necesitas instalar nada manualmente.

---

# 📁 Estructura del repositorio

```
.
├── goodrich/        # Código fuente del libro (NO modificar)
├── notebooks/       # Notebooks de clase con teoría (NO modificar)
├── exercises/       # Enunciados de ejercicios (NO modificar)
└── student_work/    # ← TU TRABAJO VA AQUÍ
```

---

# ⚠️ Reglas importantes

🔴 **NO modifiques:**

- `goodrich/`
- `notebooks/`
- `exercises/`

🟢 **Trabaja únicamente en:**

```
student_work/
```

El profesor **nunca** modifica esa carpeta. Tu trabajo ahí está siempre seguro.

---

# 🛠️ Configuración única (solo si ya tienes un Codespace creado)

Si tu Codespace no aplica automáticamente esta configuración, ejecuta este comando **una sola vez** en la terminal del Codespace:

```bash
git config merge.ours.driver true
```

Esto evita conflictos cuando el profesor actualiza los notebooks del curso.

---

# 🔄 Actualizar el contenido del curso

Cuando el profesor publique material nuevo, debes traer esos cambios a tu fork.

## Paso 1 — Conectar con el repositorio del profesor (solo una vez)

```bash
git remote add upstream https://github.com/arleyfernandotorresgalindo/EstructuraDatos_2026_02.git
```

## Paso 2 — Traer actualizaciones

```bash
git fetch upstream              # Trae lo del profe
git rebase upstream/master      # Te pones al día
git submodule update            # Actualiza el código del libro (goodrich/)
git push origin master --force  # Subes tu versión actualizada
```

👆 Esto actualiza tu fork con el material nuevo sin perder tu trabajo en `student_work/`

---

# 💾 Guardar tu trabajo

```bash
git add student_work/
git commit -m "descripción de lo que hice"
git push
```

O usa el panel **Source Control** de VS Code (ícono de rama en la barra lateral izquierda) sin escribir comandos.

---

# 📓 Uso de Jupyter

1. Ve a la carpeta `notebooks/` o `exercises/`
2. Abre un archivo `.ipynb`
3. Selecciona el kernel **Python 3.12**

---

# 🔁 Flujo de trabajo recomendado

1. Revisa la teoría en `notebooks/`
2. Lee los ejercicios en `exercises/`
3. Resuelve y guarda tu trabajo en `student_work/`
4. Haz commit y push al terminar

---

# ❓ Problemas comunes

### No aparecen cambios del profesor

```bash
git fetch upstream
git rebase upstream/master
git submodule update
git push origin master --force
```

### Error al hacer rebase (cambios locales sin guardar)

```bash
git stash
git rebase upstream/master
git stash pop
git push origin master --force
```

---

## 👨‍🏫 Autor

Curso diseñado por **Arley Fernando Torres Galindo**.
