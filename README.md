# Actividad 5 – Programación Orientada a Objetos 2026-2

**Estudiante:** Nairalzaurak Ruiz López
**Docente:** Walter Hugo Arboleda Mazo
**Universidad:** Universidad Nacional de Colombia
**Valor:** 20 % · **Fecha de entrega:** 26 de noviembre de 2026 (PDF)
**Correo de envío:** ia.walterarboleda@gmail.com
**Texto guía:** *Ejercicios de Programación Orientada a Objetos con Java y UML* – Leonardo Bermón Angarita

---

## Ejercicios realizados

Ambos ejercicios se desarrollaron con interfaz gráfica de usuario (GUI), sin hacer la parte propuesta de cada enunciado.

| Ejercicio | Título | Página | Descripción |
|-----------|--------|--------|-------------|
| 8.4 | Cuadros de diálogo (Nómina) | 517 | Calcula la nómina de los empleados de una empresa, con menú, formulario, tabla y guardado en `Nomina.txt`. |
| 8.5 | Gestión de contenidos (Hotel) | 546 | Gestiona el ingreso y la salida de huéspedes de un hotel de 10 habitaciones. |

---

## Estructura de la carpeta

```
Actividad5/
├── README.md
├── python/
│   ├── ejercicio_8_4_nomina.py   ← Ejercicio 8.4 en Python (tkinter)
│   └── ejercicio_8_5_hotel.py    ← Ejercicio 8.5 en Python (tkinter)
├── ejercicio_8_4_nomina/src/nomina/   ← Ejercicio 8.4 en Java (Swing)
├── ejercicio_8_5_hotel/src/hotel/     ← Ejercicio 8.5 en Java (Swing)
└── diagramas/
    ├── clases_8_4_nomina.puml
    ├── casos_uso_8_4_nomina.puml
    ├── clases_8_5_hotel.puml
    └── casos_uso_8_5_hotel.puml
```

---

## Ejercicio 8.4 – Nómina

**Enunciado resumido:** programa con barra de menús que permite:

1. **Agregar empleado:** nombre, apellidos, cargo (directivo, estratégico u operativo), género, salario por día, días trabajados (1 a 31), otros ingresos, pagos por salud y aporte a pensiones.
2. **Calcular nómina:** tabla con nombre, apellidos y sueldo de cada empleado, y el total de la nómina en la parte inferior.
   - Salario mensual = (días trabajados × salario por día) + otros ingresos − pagos por salud − aporte pensiones
3. **Guardar archivo:** crea `Nomina.txt` en la carpeta seleccionada con los datos, el sueldo de cada empleado y el total.

**Ejecución (Python):**
```bash
python python/ejercicio_8_4_nomina.py
```

**Ejecución (Java):** abrir `ejercicio_8_4_nomina` en VS Code con la extensión de Java y ejecutar `VentanaPrincipal`.

**Enlace GitHub:** `https://github.com/USUARIO/REPOSITORIO` *(reemplazar por el enlace real)*

---

## Ejercicio 8.5 – Hotel

**Enunciado resumido:** el hotel tiene 10 habitaciones simples. Las habitaciones 1 a 5 cuestan $120 000 por día y las 6 a 10 cuestan $160 000 por día. El programa tiene dos opciones de menú:

1. **Consultar habitaciones:** muestra cada habitación con su estado (*Disponible* / *No disponible*). Se elige una habitación libre y se registra el ingreso con fecha, nombre, apellidos y número de documento. Todos los campos son obligatorios y se validan.
2. **Salida de huéspedes:** se indica la habitación ocupada y la fecha de salida, que debe ser posterior a la de ingreso. Luego se calcula el número de días y el total a pagar, y con *Registrar salida* la habitación queda disponible.

**Ejecución (Python):**
```bash
python python/ejercicio_8_5_hotel.py
```

**Ejecución (Java):** abrir `ejercicio_8_5_hotel` en VS Code con la extensión de Java y ejecutar `VentanaPrincipalHotel`.

**Enlace GitHub:** `https://github.com/USUARIO/REPOSITORIO` *(reemplazar por el enlace real)*

---

## Diagramas

Los diagramas están en formato PlantUML dentro de la carpeta `diagramas/`. Para generar la imagen:

1. Abrir [plantuml.com/plantuml](https://www.plantuml.com/plantuml).
2. Pegar el contenido del archivo `.puml`.
3. Descargar la imagen en PNG o SVG e insertarla en el PDF.

| Archivo | Contenido |
|---------|-----------|
| `clases_8_4_nomina.puml` | Diagrama de clases del ejercicio 8.4 |
| `casos_uso_8_4_nomina.puml` | Diagrama de casos de uso del ejercicio 8.4 |
| `clases_8_5_hotel.puml` | Diagrama de clases del ejercicio 8.5 |
| `casos_uso_8_5_hotel.puml` | Diagrama de casos de uso del ejercicio 8.5 |

---

## Entregable (PDF)

- [ ] Portada con nombre, asignatura, docente y fecha
- [ ] Ejercicio 8.4: enlace de GitHub, capturas de la interfaz, diagrama de clases y diagrama de casos de uso
- [ ] Ejercicio 8.5: enlace de GitHub, capturas de la interfaz, diagrama de clases y diagrama de casos de uso
- [ ] Revisar que los enlaces funcionen y que las imágenes se vean bien
- [ ] Enviar a **ia.walterarboleda@gmail.com** antes del **26 de noviembre de 2026**

---

## Requisitos

- **Python:** 3.8 o superior (incluye tkinter).
- **Java (opcional):** JDK 8 o superior y VS Code con la extensión *Extension Pack for Java*.
