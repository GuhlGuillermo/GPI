# Sabor del Himalaya - Aplicación de Entrega de Comida 🍽️🗻

Bienvenido al repositorio de **Sabor del Himalaya**. Este proyecto consiste en una aplicación web completa orientada a la entrega de comida a domicilio, con gestión de menú diario, sistema de carrito, área de clientes y panel de administración para gestión de platos o pedidos.

El código base se encuentra dividido principalmente en una aplicación "Frontend" y un "Backend", desplegados a través de contenedores Docker. 

A continuación, encontrarás toda la información pertinente para entender, ejecutar y modificar este proyecto siguiendo las directrices de arquitectura en base al **Stack Tecnológico** empleado y una **Arquitectura Limpia (Clean Architecture)**.

---

## 🛠️ Stack Tecnológico

El proyecto se despliega unificando múltiples herramientas modernas que garantizan un desarrollo ágil, rápido y escalable.

- **Frontend:**
  - **React 18:** Librería principal para interfaces reactivas.
  - **Vite:** Herramienta de compilación ultrarrápida (`vite.config.js`) y servidor de desarrollo local.
  - **Tailwind CSS:** Framework de CSS utilizando utilidades directamente en el marcado HTML/JSX para estilado (`tailwind.config.js`).

- **Backend:**
  - **Flask:** Framework ligero de Python (`app.py`), utilizado para exponer la API REST, con autenticación segura por PyJWT.
  - **Pytest:** Framework de Testing ágil para Python, que permite testear casos de uso y la infraestructura con inyección de dependencias.

- **Base de Datos:**
  - **MongoDB:** Base de datos NoSQL documental, flexible y rápida para nuestro modelo de negocio.

- **Infraestructura:**
  - **Docker & Docker Compose:** Contenerización de cada servicio (`api_backend`, `web_frontend`, `mongo`) permitiendo replicar el entorno en cualquier máquina con un solo comando.

---

## 🏗️ Arquitectura Limpia (Clean Architecture)

El backend de este proyecto ha sido diseñado siguiendo una estructura de **Arquitectura Limpia** para separar responsabilidades y facilitar las pruebas unitarias. Si vas a modificar el código fuente del backend (`Proyecto/backend/src`), debes tener en cuenta las siguientes capas:

1. **`domain/` (Dominio y Modelos de Datos)**:
   - Aquí residen los modelos de negocio puros, escritos como _dataclasses_ de Python (`models.py`) y las excepciones personalizadas.
   - **Regla:** Esta capa NO depende de ninguna otra. No debe importar módulos de bases de datos ni frameworks web.

2. **`use_cases/` (Casos de Uso / Lógica de Negocio)**:
   - Contiene la lógica de la aplicación (ej. "Realizar pedido", "Añadir plato", "Registrar usuario"). 
   - Utilizan los modelos de dominio y las interfaces (puertos) para interactuar con datos.
   - **Regla:** Dependen del dominio, pero nunca de la base de datos o el framework web.

3. **`interfaces/` (Controladores y Rutas)**:
   - Controladores de Flask y configuración de Blueprints. Son los encargados de recibir las peticiones HTTP, parsear los JSON y llamar al Caso de Uso apropiado.
   - **Regla:** Sirven de puente exterior hacia nuestros `use_cases`.

4. **`infrastructure/` (Infraestructura / Persistencia)**:
   - Implementa los repositorios (patrón *Repository*) para comunicarse con la base de datos específica (en este caso, **MongoDB** a través de PyMongo).
   - **Regla:** Conoce la base de datos y provee métodos para almacenar o recuperar las de las colecciones de base de datos hacia las Data Classes de `domain/`.

### 💻 Guía para editar el Backend
- Si necesitas **cambiar la estructura de un dato** -> Modifica `domain/models.py`.
- Si necesitas **una nueva regla de negocio** -> Crea / Modifica el archivo pertinente en `use_cases/`.
- Si necesitas **un nuevo Endpoint HTTP** -> Define la ruta en un controlador en `interfaces/` y llama al caso de uso correspondiente.
- Si necesitas **nuevas consultas a Base de Datos** -> Añade los métodos en el repositorio de `infrastructure/`.

### 💻 Guía para editar el Frontend
Ubicado en `Proyecto/frontend/src/`, este entorno sigue una arquitectura modular en base a _Features_ (funcionalidades):
- **`features/`**: Contiene la lógica por funcionalidad (por ejemplo, `admin`, `cart`, `auth`, `menu`, `home`). Si buscas un componente sobre el menú de platos, lo encontrarás en `features/menu`.
- **`core/`**: Componentes globales o servicios transversales que pueden ser reutilizados por diversas _features_.
- Usa las clases utilitarias de Tailwind en el JSX para el control de estilos, centralizadas si es necesario en `index.css`. Las variables del entorno (como URLs de la API) se definen con de la convención de Vite, prefijadas por `VITE_`.

---

## 🗃️ Modelo de Datos

A continuación se detalla la base y los flujos de las entidades centrales registradas en `domain/models.py` (y almacenadas en MongoDB):

*   **`User` (Usuario)**: Representa a los clientes y al personal administrativo.
    *   Campos: `id_usuario`, `nombre`, `email`, `contraseña` (hash), `gasto_total`, `es_cliente_habitual`, `rol` ("CLIENT" o "ADMIN").
*   **`Dish` (Plato)**: Refleja un elemento del catálogo gastronómico.
    *   Campos: `id_plato`, `nombre_plato`, `descripcion`, `precio_plato`, `categoria` ("ENTRANTE", "PRINCIPAL", "POSTRE"), `es_de_temporada` (booleano), `url_imagen`, `activo`.
*   **`Menu` (Menú del Día)**: Un conjunto de platos elegidos para una fecha en concreto. 
    *   Campos: `id_menu`, `fecha`, y arreglos de referencias a IDs de platos: `entrantes`, `platos_principal`, `postres`. Define también `precio_menu`.
*   **`Order` (Pedido)**: Gestiona las ventas y transacciones.
    *   Campos: `id_pedido`, `id_usuario` (referencia al que compró), `items` (lista de `OrderItem` conteniendo id_plato, nombre, precio por unidad y cantidad), `importe_total`, `estado` (EJ: "RECIBIDO", "PREPARANDO", "ENTREGADO"), `dir_entrega`, `hora_entrega`, `info_pago`.

---

## 🚀 Despliegue y Ejecución

Al contar con el archivo de configuración en la raíz del proyecto, levantar el sistema completo es muy sencillo y automatizado.

### Requisitos Previos:
- Tener instalado **Docker** y **Docker Compose**.

### Montar los contenedores:
1. Abre una terminal y dirígete al directorio raíz (`Proyecto/`).
2. Ejecuta el comando de Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Docker orquestará los 3 servicios:
   - **Frontend (Vite)** accesible en: `http://localhost:5173`
   - **Backend API (Flask)** accesible en: `http://localhost:5000`
   - **Base de Datos MongoDB** expuesta en el puerto: `27017`

### Ejecución de Pruebas Automáticas (Pytest)
Para pasar la batería de pruebas en el entorno de backend, dirígete al directorio de \`backend\` e invoca pytest:

1. Crea o activa un entorno virtual (recomendado) en python.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta los tests: `pytest` 

_(Alternativamente, se puede ejecutar \`pytest\` montándolo en el entorno de Docker si se desea)._