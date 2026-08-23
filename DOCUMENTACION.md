# Sistema de Ordenes

Aplicacion web para registrar, consultar y dar seguimiento a ordenes de venta. El sistema esta construido con Django, utiliza SQLite por defecto y puede ejecutarse localmente con el servidor de desarrollo o mediante Waitress en Windows.

## Indice

1. [Parte 1: Instalacion en otra PC](#parte-1-instalacion-en-otra-pc)
2. [Parte 2: Funciones de la aplicacion](#parte-2-funciones-de-la-aplicacion)
3. [Parte 3: Detalles tecnicos y mantenimiento](#parte-3-detalles-tecnicos-y-mantenimiento)

---

## Parte 1: Instalacion en otra PC

### 1.1 Requisitos previos

- Windows 10 u 11.
- Python compatible con Django 6; se recomienda Python 3.12 o posterior.
- Acceso a Internet durante la instalacion de paquetes.
- Permisos para abrir el puerto TCP 8000 si otros equipos accederan al sistema.
- Todos los archivos del proyecto, conservando la estructura de carpetas.

La carpeta `.venv` no es necesario copiarla. Es preferible crear un entorno virtual nuevo en la PC de destino.

### 1.2 Copiar el proyecto

Copie la carpeta completa del proyecto, incluyendo como minimo:

- `manage.py`
- `requirements.txt`
- Las carpetas `sistema`, `ordenes`, `usuarios`, `templates` y `static`.
- `media` si se desea conservar los PDFs ya cargados.
- `db.sqlite3` si se desea conservar los usuarios, ordenes y registros existentes.
- `iniciar_sistema.bat` para iniciar el sistema con doble clic.

Si se omite `db.sqlite3`, se creara una base de datos nueva al ejecutar las migraciones.

### 1.2.1 Que se incluye al clonar desde GitHub

El repositorio contiene el codigo fuente, las plantillas, los archivos estaticos fuente, las migraciones, `requirements.txt`, `.env.example` y esta documentacion. Por seguridad, no contiene:

- `.env` ni `.env.local`.
- Entornos virtuales como `.venv` o `venv`.
- `db.sqlite3` ni otros archivos SQLite.
- PDFs y otros archivos dentro de `media`.
- `staticfiles`, `__pycache__` ni archivos `.pyc`.

Por eso, despues de clonar hay que crear el entorno virtual, instalar dependencias y ejecutar las migraciones. Si se necesita conservar la informacion de una instalacion existente, copie por separado `db.sqlite3` y la carpeta `media` desde la PC anterior, con el servidor detenido.

Para configurar variables locales, copie la plantilla:

```powershell
Copy-Item .env.example .env.local
```

Edite `.env.local` en la PC destino. El archivo real permanece ignorado por Git y no debe subirse al repositorio.

### 1.3 Crear el entorno virtual

Abra PowerShell o CMD dentro de la carpeta del proyecto y ejecute:

```powershell
py -m venv .venv
```

Active el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activacion por politica de ejecucion, puede usar CMD:

```bat
.venv\Scripts\activate.bat
```

Tambien puede continuar sin activar el entorno y utilizar siempre la ruta `.venv\Scripts\python.exe`.

### 1.4 Instalar las dependencias

Con el entorno activo, ejecute:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Entre las dependencias principales se encuentran Django, Waitress y WhiteNoise. El archivo `requirements.txt` contiene tambien paquetes adicionales utilizados por el entorno actual.

### 1.5 Preparar la base de datos

Ejecute las migraciones:

```powershell
python manage.py migrate
```

Compruebe que la configuracion de Django sea valida:

```powershell
python manage.py check
```

Si necesita crear un administrador nuevo, use el comando oficial de Django:

```powershell
python manage.py createsuperuser
```

El programa solicitara nombre de usuario, correo y contraseña.

Tambien existe el archivo `crear_usuario.py`, que crea un usuario de prueba llamado `admin` con la contraseña `admin123` cuando no existe. Esas credenciales son conocidas y solo deben utilizarse en pruebas; cambielas o cree un superusuario propio antes de usar el sistema en produccion.

### 1.6 Configurar roles y permisos

Para crear o actualizar los grupos `admin`, `capturista` y `lector`, ejecute:

```powershell
python manage.py setup_roles
```

El comando asigna los permisos de ordenes a cada grupo. Despues, desde la pantalla **Usuarios**, un administrador puede crear usuarios y asignarles un rol.

Existe tambien `scripts\setup_roles_and_users.py`, que configura los grupos y crea el usuario `capturista1` con una contraseña de prueba si no existe. Utilicelo solo para ambientes de prueba:

```powershell
python scripts\setup_roles_and_users.py
```

### 1.7 Iniciar la aplicacion

#### Opcion recomendada en Windows

Haga doble clic en `iniciar_sistema.bat`. El archivo:

1. Se posiciona en la carpeta del proyecto.
2. Comprueba que exista `.venv\Scripts\python.exe`.
3. Inicia Waitress en `0.0.0.0:8000`.
4. Abre el navegador en `http://127.0.0.1:8000`.

Tambien puede iniciarlo manualmente:

```powershell
.venv\Scripts\python.exe -m waitress --host=0.0.0.0 --port=8000 sistema.wsgi:application
```

Mantenga abierta la ventana del servidor mientras utilice la aplicacion.

#### Opcion de desarrollo

Para desarrollo y depuracion:

```powershell
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`.

### 1.8 Acceso desde otra PC de la red

El servidor escucha en todas las interfaces mediante `0.0.0.0`, pero la PC cliente debe acceder usando la IP de la PC donde corre Django:

```text
http://IP_DE_LA_PC_SERVIDORA:8000/
```

Para consultar la IP en Windows:

```powershell
ipconfig
```

Antes de probar desde otra PC:

1. Permita Python o el puerto 8000 en el Firewall de Windows.
2. Configure `ALLOWED_HOSTS` con la IP real de la PC servidora.
3. Verifique que ambas PC esten en la misma red.

La configuracion actual incluye algunas direcciones predeterminadas, pero una IP distinta puede producir el error **DisallowedHost**. La forma recomendada es crear `.env.local` en la raiz del proyecto con:

```text
ALLOWED_HOSTS=localhost,127.0.0.1,IP_DE_LA_PC_SERVIDORA
```

El archivo `.env.local` es leido por `sistema/settings.py` y no debe publicarse si contiene secretos.

### 1.9 Configuracion opcional mediante `.env.local`

Se pueden definir estos valores:

```text
SECRET_KEY=una-clave-larga-y-privada
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=America/Denver
```

Para una base de datos distinta de SQLite tambien existen:

```text
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=C:/ruta/al/proyecto/db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

La configuracion por defecto utiliza `db.sqlite3` en la raiz del proyecto.

### 1.10 Comprobacion final de instalacion

Ejecute esta secuencia antes de entregar la PC:

```powershell
python manage.py check
python manage.py migrate --check
python manage.py collectstatic --noinput
```

Despues inicie el BAT, abra `http://127.0.0.1:8000/` e inicie sesion. Pruebe crear una orden, consultar el dashboard y cerrar sesion.

---

## Parte 2: Funciones de la aplicacion

### 2.1 Inicio de sesion y cierre de sesion

La pagina inicial requiere autenticacion. El usuario introduce nombre y contraseña; Django valida las credenciales y redirige al dashboard. Las credenciales incorrectas muestran un mensaje de error.

La opcion **Cerrar sesion** invalida la sesion actual y devuelve al formulario de login. Las paginas protegidas redirigen automaticamente a `/login/` si se accede sin autenticacion.

### 2.2 Dashboard

La pantalla **Inicio** (`/dashboard/`) muestra un resumen de la operacion:

- Ordenes pendientes.
- Ordenes en proceso.
- Ordenes completas.
- Total de ordenes con factura.
- Ordenes creadas hoy.
- Ordenes creadas durante la semana actual.
- Ordenes creadas durante el mes actual.

Los totales se calculan directamente desde la base de datos y utilizan la fecha local configurada en `TIME_ZONE`.

### 2.3 Captura y consulta de ordenes

La pantalla **Captura de datos** (`/`) permite registrar una orden con los siguientes datos:

- Usuario o responsable asociado.
- Numero de orden.
- Fecha de la orden.
- Fecha de factura.
- Fecha de termino.
- Numero de factura.
- Descripcion.
- Estatus: `pendiente`, `proceso` o `completo`.
- Comentarios.
- Archivo PDF opcional.

El numero de factura debe ser numerico. Los campos de fecha, factura, PDF, descripcion y comentarios pueden quedar vacios.

La tabla de registros permite:

- Buscar por usuario.
- Buscar por numero de orden.
- Buscar por factura.
- Filtrar por estatus.
- Filtrar por fecha de inicio y fecha final.
- Filtrar por fecha de factura.
- Navegar por paginas de ocho ordenes.
- Abrir un modal con el detalle completo.
- Editar una orden cuando el usuario tiene permiso.
- Eliminar una orden cuando el usuario tiene permiso.
- Consultar el PDF adjunto cuando existe.

### 2.4 Detalle y edicion de orden

La vista de detalle (`/ver/<id>/`) muestra la informacion completa de una orden. El propietario, un superusuario o un usuario con permiso global de consulta puede verla.

La edicion puede realizarse desde la pantalla principal o desde el formulario completo (`/editar/<id>/`). Tambien existe una edicion en modal que actualiza la informacion mediante una solicitud AJAX (`/editar_modal/<id>/`). Al editar se puede reemplazar el PDF adjunto.

### 2.5 Reportes

La pantalla **Reportes** (`/reportes/`) permite filtrar las ordenes por:

- Texto de usuario.
- Fecha inicial.
- Fecha final.

Muestra:

- Total de ordenes.
- Facturas registradas.
- Ordenes pendientes.
- Ordenes en proceso.
- Ordenes completadas.
- Grafica de ordenes por mes.
- Grafica de ordenes por usuario.
- Grafica de distribucion por estatus.

Las graficas se dibujan con Chart.js cargado desde CDN, por lo que el navegador necesita acceso a Internet para mostrar esa parte visual.

### 2.6 Gestion de usuarios

La pantalla **Usuarios** permite a un administrador:

- Crear usuarios.
- Asignar los roles `admin`, `capturista` o `lector`.
- Editar el nombre de usuario y el rol.
- Eliminar usuarios que no sean superusuarios.

El usuario conectado no puede eliminarse a si mismo. Un usuario que no sea superusuario tampoco puede editar ni eliminar un superusuario.

### 2.7 Roles y permisos

| Rol | Funciones principales |
|---|---|
| `admin` | Crear, consultar, editar y eliminar ordenes; consultar todas las ordenes; administrar usuarios; consultar actividad. |
| `capturista` | Crear y editar ordenes; consultar los registros disponibles. |
| `lector` | Consultar ordenes y reportes, sin crear, editar ni eliminar. |
| Superusuario | Acceso administrativo completo de Django y acceso total a la aplicacion. |

Los permisos de ordenes definidos por el proyecto son:

- `can_create_order`
- `can_edit_order`
- `can_delete_order`
- `can_view_all_orders`

Los controles de permiso se aplican tanto en la interfaz como en las vistas del servidor. Ocultar un boton no sustituye la validacion del servidor.

### 2.8 Actividad y auditoria

La pantalla **Actividad** esta disponible para superusuarios y usuarios del grupo `admin`. Permite filtrar movimientos por usuario y fecha.

El sistema registra acciones de administracion de usuarios, como creacion, edicion y eliminacion. Adicionalmente, las señales de Django registran en `ActivityLog` los eventos de creacion, actualizacion y eliminacion de modelos de la aplicacion `ordenes`.

Las ordenes conservan tambien usuario y fechas de creacion/actualizacion mediante `AuditMixin` cuando la accion se ejecuta dentro de una solicitud web autenticada.

### 2.9 Apariencia y experiencia de uso

La interfaz utiliza Bootstrap, Font Awesome, DataTables y hojas de estilo propias. Incluye:

- Modo claro y modo oscuro.
- Preferencia de tema guardada en el navegador.
- Menu lateral adaptable a pantallas pequenas.
- Tablas con busqueda y ordenamiento donde corresponde.
- Modales de confirmacion para acciones destructivas.
- Diseño responsive para escritorio y movil.

---

## Parte 3: Detalles tecnicos y mantenimiento

### 3.1 Estructura principal

```text
manage.py                 Entrada para comandos Django
sistema/                  Configuracion, URLs, WSGI y ASGI
ordenes/                  Modelo Orden, vistas y permisos de ordenes
usuarios/                 Login, dashboard, usuarios, actividad y reportes
templates/                Plantillas HTML de la interfaz
static/                   CSS y JavaScript propios
media/pdfs/               PDFs cargados por los usuarios
db.sqlite3                Base de datos local por defecto
requirements.txt          Dependencias Python
iniciar_sistema.bat       Inicio de Waitress en Windows
```

### 3.2 Modelos de datos

`Orden` contiene la informacion operativa de cada orden, el PDF opcional y los campos de auditoria heredados de `AuditMixin`.

`Actividad` registra acciones administrativas de usuarios con usuario, accion, descripcion y fecha/hora.

`ActivityLog` registra eventos genericos de creacion, actualizacion y eliminacion de modelos de la aplicacion `ordenes`.

La autenticacion utiliza el modelo incorporado `django.contrib.auth.models.User`, junto con grupos y permisos de Django.

### 3.3 Migraciones

Las migraciones se encuentran en `ordenes/migrations` y `usuarios/migrations`. Cada vez que se modifiquen los modelos:

```powershell
python manage.py makemigrations
python manage.py migrate
```

No borre `db.sqlite3` ni las migraciones existentes para corregir un error de instalacion; primero revise el mensaje mostrado por Django.

### 3.4 Archivos estaticos y archivos subidos

Los recursos CSS y JavaScript propios estan en `static`. Django los sirve durante el desarrollo. Para una ejecucion preparada para produccion:

```powershell
python manage.py collectstatic --noinput
```

Los PDFs se guardan en `media/pdfs`. Esta carpeta debe incluirse en las copias de seguridad. En modo `DEBUG=True`, Django publica los archivos media y static mediante las rutas configuradas en `sistema/urls.py`. WhiteNoise se utiliza para los archivos estaticos cuando `DEBUG=False`.

### 3.5 Copias de seguridad

Para conservar la informacion, respalde como minimo:

- `db.sqlite3`.
- `media/pdfs/`.
- `.env.local`, si existe, guardandolo de forma privada.

Detenga el servidor antes de copiar `db.sqlite3` para reducir el riesgo de una copia inconsistente. No sustituya una base de datos en uso sin tener primero una copia de seguridad.

### 3.6 Diagnostico rapido

**El BAT indica que no encuentra el entorno virtual**

Ejecute `py -m venv .venv` desde la raiz del proyecto y vuelva a instalar las dependencias.

**No se reconoce Waitress**

Ejecute:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Aparece `No module named whitenoise`**

La instalacion de dependencias esta incompleta. Repita el comando anterior.

**Aparece `DisallowedHost`**

Agregue el nombre o la IP utilizados para acceder a `ALLOWED_HOSTS` en `.env.local` y reinicie el servidor.

**La pantalla carga sin estilos o sin graficas**

Compruebe `collectstatic`, la carpeta `staticfiles` y la conexion a Internet para los recursos externos de Bootstrap, DataTables, Font Awesome y Chart.js.

**El puerto 8000 esta ocupado**

Identifique el proceso que lo utiliza o cambie el puerto en `iniciar_sistema.bat` y en la URL de acceso. Por ejemplo, use `--port=8010` y abra `http://127.0.0.1:8010`.

### 3.7 Consideraciones de seguridad para produccion

- Cambie `SECRET_KEY`; no utilice la clave predeterminada.
- Use `DEBUG=False`.
- Configure `ALLOWED_HOSTS` de forma explicita.
- Cambie las contraseñas de prueba.
- Restrinja el acceso al puerto 8000 mediante el Firewall.
- Haga copias de seguridad de la base de datos y de los PDFs.
- Considere migrar de SQLite a un motor de base de datos servidor si varios usuarios escribiran simultaneamente o el volumen de datos crece.
- Revise el servidor web y HTTPS antes de exponer la aplicacion fuera de la red local.

### 3.8 Comandos utiles

```powershell
python manage.py check                 # Comprueba la configuracion
python manage.py migrate               # Aplica migraciones
python manage.py showmigrations        # Muestra el estado de migraciones
python manage.py createsuperuser       # Crea un administrador
python manage.py setup_roles            # Configura grupos y permisos
python manage.py populate_test_orders   # Crea 50 ordenes de prueba
python manage.py collectstatic --noinput # Reune archivos estaticos
```

`populate_test_orders` genera informacion ficticia y no debe ejecutarse sobre una base de datos productiva sin una copia previa.

### 3.9 Rutas principales

| Ruta | Funcion |
|---|---|
| `/` | Captura y listado de ordenes |
| `/login/` | Inicio de sesion |
| `/logout/` | Cierre de sesion |
| `/dashboard/` | Dashboard |
| `/usuarios/` | Gestion de usuarios |
| `/actividad/` | Bitacora administrativa |
| `/reportes/` | Reportes y graficas |
| `/ver/<id>/` | Detalle de una orden |
| `/editar/<id>/` | Edicion de una orden |
| `/admin/` | Administracion interna de Django |

---

## Resumen de instalacion

En una PC nueva, la secuencia minima es:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py setup_roles
python manage.py check
```

Luego ejecute `iniciar_sistema.bat` y abra `http://127.0.0.1:8000/`.