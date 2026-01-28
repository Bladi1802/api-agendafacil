# AgendaFacil API (Django REST + PostgreSQL + React)

AgendaFacil es una API REST para gestionar citas de negocios por reservación (taller mecánico, barbería, salón de belleza, salón de eventos). Centraliza la agenda, evita traslapes, administra servicios y clientes, y permite seguimiento por estados de cita.

---

## Stack (decisión tecnológica)
- Backend: Django + Django REST Framework
- Database: PostgreSQL
- Frontend: React (Vite)
- Extras: django-cors-headers, python-dotenv

**Justificación breve:** DRF es estándar en industria para APIs REST en Python. PostgreSQL ofrece integridad relacional ideal para agendas (citas, servicios y relaciones). React permite construir un frontend moderno desacoplado del backend.

---

## Alcance (Scope) y Recursos (MVP)

### Recursos principales
1) users
2) businesses
3) services
4) customers
5) appointments

### Operaciones REST planeadas (ejemplos)
**Businesses**
- GET /api/businesses
- POST /api/businesses
- GET /api/businesses/{id}
- PUT /api/businesses/{id}

**Services**
- GET /api/services
- POST /api/services
- GET /api/services/{id}

**Customers**
- GET /api/customers
- POST /api/customers

**Appointments**
- GET /api/appointments
- POST /api/appointments
- GET /api/appointments/{id}
- PATCH /api/appointments/{id} (cambiar estado)

---

## Reglas de negocio
- No se puede agendar una cita en el pasado.
- Un negocio no puede tener dos citas en el mismo horario (sin traslape).
- Una cita debe estar asociada a un negocio y a un servicio.
- El estado de una cita solo puede avanzar: pending → confirmed → completed (o canceled).
- La duración de la cita se calcula con base en la duración del servicio.
- (Opcional) Un cliente no puede tener dos citas a la misma hora (aunque sean negocios distintos).

---

## Contrato preliminar (simple)

### Endpoint propuesto 1
**POST /api/appointments**
Request (mock):
```json
{
  "business_id": 1,
  "service_id": 3,
  "customer_id": 10,
  "start_time": "2026-02-01T10:00:00",
  "notes": "Cliente solicita atención rápida"
}

## Configuración de rutas y controladores

Esta sección documenta cómo se configuraron los endpoints iniciales de AgendaFacil con una separación mínima de responsabilidades (rutas vs lógica), siguiendo una estructura replicable.

### A) Estructura y responsabilidades

- Backend (Django REST Framework):
backend/
agendafacil/ # Configuración del proyecto (settings/urls)
api/ # App principal de la API
urls.py # Rutas (endpoints) de la app
controllers/ # Controladores (lógica por recurso)
health_controller.py
services_controller.py
---


**¿Por qué separar rutas y controladores?**
- `urls.py` se mantiene limpio y solo define rutas.
- `controllers/` concentra la lógica, facilitando mantenimiento y escalabilidad.
- Permite agregar nuevos recursos sin ensuciar el routing.

---

### B) Paso a paso técnico

1. Se creó la carpeta `api/controllers/` para almacenar la lógica.
2. Se definieron funciones controlador por recurso:
   - `health_controller.py`: verificación de estado del API.
   - `services_controller.py`: endpoints mock para listar y crear servicios.
3. Se registraron rutas en `api/urls.py` y se conectaron a los controladores.
4. Se incluyó `path("api/", include("api.urls"))` en `agendafacil/urls.py` para exponer las rutas bajo `/api/`.

> Nota: Para esta actividad no se requiere base de datos. Los endpoints de services usan datos mock en memoria.

---

### C) Endpoints implementados

#### 1) Health check
- **Método:** GET  
- **Ruta:** `/api/health/`  
- **Descripción:** Devuelve el estado del servidor y el nombre del proyecto.
- **Respuesta (ejemplo):**
```json
{
  "status": "ok",
  "project": "AgendaFacil"
}


