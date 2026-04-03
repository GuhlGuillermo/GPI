# Proyecto GastroTech - Clean Architecture en Django

Este repositorio contiene la estructura esqueleto de GastroTech, una aplicación Web desarrollada en **Django**, enfocada en mantener las reglas de negocio aisladas de los detalles de infraestructura utilizando **Clean Architecture**. Se integra **MongoDB** como base de datos persistente mediante PyMongo y una interfaz de usuario fluida y moderna utilizando **TailwindCSS** y **HTMX**.

## Índice
1. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
2. [Flujo de la Aplicación](#flujo-de-la-aplicación)
3. [Explicación del Código y Capas](#explicación-del-código-y-capas)
4. [Instrucciones de Despliegue](#instrucciones-de-despliegue)
5. [Guía para Modificar y Extender](#guía-para-modificar-y-extender)

---

## Arquitectura del Proyecto

Hemos implementado una variante modularizada de la Arquitectura Limpia (*Clean Architecture* de Robert C. Martin). El principio fundamental es la *Regla de Dependencia*: el código de las capas internas no puede depender de nada de las capas externas.

Estructura de directorios principal:
```text
Proyecto/
├── core/             - Configuraciones nativas de Django (settings.py, urls.py).
├── domain/           - Entidades del negocio puras e Interfaces Genuinas. (Capa Interna)
├── use_cases/        - La lógica de negocio e interacción entre entidades.
├── infrastructure/   - Detalles concretos de la DB (MongoDB con PyMongo). (Capa Externa)
├── delivery/         - Vistas de Django, rutas locales y HTML (Tailwind+HTMX). (Capa Externa)
└── manage.py         - Punto de entrada de Django.
```

---

## Flujo de la Aplicación

Cuando un cliente interactúa con la aplicación (por ejemplo, cargando la carta de Platos con HTMX), ocurre lo siguiente:

1. **Delivery (Vista Django):** El usuario pulsa "Ver Carta". HTMX envía una petición GET a la URL de Django conectada en `delivery/views.py` (`platos_list()`).
2. **Controlador:** La vista recibe la request. Ésta no llama directamente a la base de datos, sino que insta a la capa de `Casos de Uso` proveyéndole la interfaz adecuada (e.g. `MongoCatalogoRepository`).
3. **Casos de Uso (Use Cases):** `ConsultarCatalogoUseCase` se ejecuta. Solo entiende las interfaces del Dominio (no sabe que es MongoDB o Django). Simplemente le dice al Repositorio inyectado: `listar_platos_en_carta()`.
4. **Infraestructura (MongoRepo):** El repositorio ejecuta una query real en MongoDB (`collection.find()`), extrae los documentos libres de metadatos extra y construye instancias de la capa más profunda: `Plato` (entidad pura).
5. **Retorno Escalonado:** Entidad -> Caso de Uso -> Vista. La vista inyecta las entidades en la plantilla parcial renderizada (`partials/plato_list.html`).
6. **HTMX Dibuja UI:** El HTML generado se devuelve al cliente y HTMX reemplaza el bloque en la página original sin recargar, manteniendo transiciones animadas con Tailwind.

---

## Explicación del Código y Capas pormenorizada

### 1. Dominio (`domain/entities.py`, `domain/repository_interfaces.py`)
Contiene clases planas construidas con `@dataclass`. No heredan de `django.db.models.Model` porque de hacerlo estaríamos atando nuestras reglas de negocio al ORM de Django.
**¿Por qué está así?** Para asegurar que si mañana se cambia MongoDB por PostgreSQL, las entidades ni se enteren, porque representan puramente "Qué datos forman un Plato".
*Interfaces*: Definidas con la clase base abstracta `ABC`. Actúan como "Puertos" entre los casos de uso y la infraestructura.

### 2. Casos de Uso (`use_cases/...`)
Se implementan como clases individuales (e.g., `CrearPedidoUseCase`). Se construyen con el principio de Inversión de Dependencias (constructor recibe `PedidoRepository` y NO `MongoPedidoRepository`). 
**¿Por qué está así?** Mantiene la regla central de negocio (ej: si se crea un pedido sin platos, lanzar error) en un entorno independiente de la UI.

### 3. Infraestructura (`infrastructure/...`)
Aquí reside la librería de terceros `pymongo`. Archivos aislados (`mongo_connection.py` y `mongo_repositories.py`).
**¿Por qué está así?** Conecta la lógica. `MongoPedidoRepository` hereda del puerto abstract `PedidoRepository` del Dominio, y traduce Dataclasses Python a Diccionarios JSON compatibles con Mongo.

### 4. Delivery/UI (`delivery/...`)
Aquí brilla TailwindCSS junto a las plantillas HTML5. Utilizamos colores de la marca, "glass panels" (paneles estilo cristal, semitransparentes), flexbox/grid layout y microanimaciones de hovers y degradados. HTMX está integrado para comportamientos *Single Page Application* sin escribir un solo archivo de React, Angular o Vue Javascript.

---

## Instrucciones de Despliegue

Los archivos facilitados (`Dockerfile`, `docker-compose.yml`, `deploy.sh`) permiten correr esto en cualquier máquina virtual.

1. Conéctese a su Máquina Virtual con Docker instalado (ej: AWS EC2, DigitalOcean Droplet).
2. Clone este repositorio: `git clone <repo>`
3. Navegue al directorio `Proyecto/`
4. Dele permisos al script: `chmod +x deploy.sh`
5. Ejecute: `./deploy.sh`

Este script levantará internamente dos contenedores en red:
- **web:** Corre Django manejado por **Gunicorn** a través del puerto 8000.
- **mongo:** Imagen de base de datos oficial corriendo en el puerto 27017, con volumen persistente salvaguardando sus datos en caso de reiniciar.

*(Nota: En un servidor de producción se recomienda añadir y mapear un proxy inverso como Nginx directamente apuntando a `web:8000`, pero se sale del alcance del esqueleto base)*

---

## Guía para Modificar y Extender

Sigue siempre estas normas para agregar funcionalidades sin romper la Arquitectura Limpia:

- **Añadir un nuevo campo al modelo de datos:**
  1. Ve a `domain/entities.py` y añada la propiedad al Dataclass.
  2. Ve a los repositorios de `infrastructure/mongo_repositories.py` para asegurar que el query coge ese nuevo campo (o por default al devolver el dict).
  3. Modifica la plantilla de `delivery/templates` si quieres mostrarlo.

- **Añadir una acción de negocio nueva (ej: Cancelar Pedido):**
  1. (Dominio) Crea la firma de interfaz en `repository_interfaces.py`: `def cancelar_pedido(...)`
  2. (Caso de Uso) Crea `CancelarPedidoUseCase` con sus validaciones de negocio "Solo puede cancelar si el estado es 'Recibido'".
  3. (Infraest.) Implementa la función dictada por interfaz actualizando MongoDB con PyMongo.
  4. (Delivery) Crea una vista Django y asóciala a una URL para ejecutar el caso de uso. Manda petición por HTMX mediante tag `<button hx-delete="...">`.
