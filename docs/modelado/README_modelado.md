# Modelado del Dominio — AgendaFácil

## 1. Breve explicación del dominio
AgendaFácil es un sistema de reservaciones/citas para negocios como barberías, salones de belleza, consultorios o talleres.
Permite que un cliente agende una cita con un negocio, seleccionando uno o varios servicios (por ejemplo: “corte” + “barba”).
El objetivo es organizar la agenda del negocio, reducir errores por duplicidad y mantener trazabilidad de citas, servicios y disponibilidad.

## 2. Decisiones clave del modelo
- Se modela `User` como entidad base para autenticación y roles (CLIENT, BUSINESS, ADMIN).
- Se modela `Business` como entidad principal del negocio. Un usuario puede ser dueño de varios negocios.
- Se modela `Service` como catálogo de servicios ofrecidos por cada negocio (duración y precio).
- La entidad principal de negocio para la operación es `Appointment` (cita/reserva).
- La relación N–N entre `Appointment` y `Service` se resuelve con una entidad puente `AppointmentService`,
  permitiendo almacenar datos de detalle como quantity y unit_price.
- Se agrega `AvailabilitySlot` para definir horarios de atención por día de semana y rangos de tiempo.
- Todas las entidades incluyen timestamps (`created_at`, `updated_at`) para auditoría.

## 3. Reglas y restricciones (integridad)
- Unique: `Service` no puede repetirse por negocio (`business + name`).
- Unique: un servicio no se puede duplicar dentro de la misma cita (`appointment + service`).
- Constraint: `Appointment.end_at` debe ser mayor que `Appointment.start_at`.
- Constraint: duración del servicio > 0 y precios >= 0.
- Constraint: day_of_week en AvailabilitySlot debe estar en 0..6.

## 4. Supuestos (assumptions)
- Un negocio pertenece a un solo usuario dueño (owner).
- Un usuario puede reservar citas en uno o varios negocios.
- La prevención avanzada de solapamientos de citas (conflictos de horario) se implementará a nivel de lógica de aplicación
  (servicios/capa de dominio), aunque existen índices para facilitar consultas por rango de tiempo.
- La disponibilidad del negocio se define por slots semanales (day_of_week + start_time/end_time).
