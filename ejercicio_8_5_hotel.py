"""
Ejercicio 8.5 - Gestion de huespedes de un hotel (interfaz grafica con tkinter).

El hotel tiene 10 habitaciones simples:
  - Habitaciones 1 a 5: $120 000 por dia.
  - Habitaciones 6 a 10: $160 000 por dia.

Menu:
  - Consultar habitaciones: muestra el estado y permite registrar un huesped.
  - Salida de huespedes: libera una habitacion calculando dias y total a pagar.

Ejecutar:  python ejercicio_8_5_hotel.py
"""
from datetime import date, datetime
import tkinter as tk
from tkinter import ttk, messagebox

NUMERO_HABITACIONES = 10


# ----------------------------------------------------------------------
# Modelo
# ----------------------------------------------------------------------
class Huesped:
    def __init__(self, nombre, apellidos, documento, fecha_ingreso):
        self.nombre = nombre
        self.apellidos = apellidos
        self.documento = documento
        self.fecha_ingreso = fecha_ingreso  # objeto date


class Habitacion:
    def __init__(self, numero, precio_dia):
        self.numero = numero
        self.precio_dia = precio_dia
        self.huesped = None

    @property
    def ocupada(self):
        return self.huesped is not None

    @property
    def estado(self):
        return "No disponible" if self.ocupada else "Disponible"

    def ocupar(self, huesped):
        self.huesped = huesped

    def liberar(self):
        self.huesped = None


class Hotel:
    def __init__(self):
        # Las primeras 5 cuestan 120 000 y las otras 5 cuestan 160 000
        self.habitaciones = [
            Habitacion(n, 120000 if n <= 5 else 160000)
            for n in range(1, NUMERO_HABITACIONES + 1)
        ]

    def get_habitacion(self, numero):
        """Retorna la habitacion o None si el numero no existe."""
        if 1 <= numero <= NUMERO_HABITACIONES:
            return self.habitaciones[numero - 1]
        return None


def convertir_fecha(texto):
    """Convierte 'aaaa-mm-dd' a date. Lanza ValueError si el formato es incorrecto."""
    return datetime.strptime(texto.strip(), "%Y-%m-%d").date()


# ----------------------------------------------------------------------
# Interfaz grafica
# ----------------------------------------------------------------------
class VentanaHabitaciones(tk.Toplevel):
    """Muestra las 10 habitaciones con su estado y permite registrar un huesped."""

    def __init__(self, master, hotel):
        super().__init__(master)
        self.hotel = hotel
        self.title("Consultar habitaciones")
        self.geometry("480x380")

        self.tabla = ttk.Treeview(self, columns=("hab", "precio", "estado"), show="headings")
        self.tabla.heading("hab", text="Habitacion")
        self.tabla.heading("precio", text="Precio por dia")
        self.tabla.heading("estado", text="Estado")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        barra = ttk.Frame(self, padding=(10, 0, 10, 10))
        barra.pack(fill="x")
        ttk.Label(barra, text="Numero de habitacion:").pack(side="left")
        self.campo_numero = ttk.Entry(barra, width=6)
        self.campo_numero.pack(side="left", padx=5)
        ttk.Button(barra, text="Registrar huesped",
                   command=self.seleccionar_habitacion).pack(side="left")

        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for h in self.hotel.habitaciones:
            self.tabla.insert("", "end", values=(h.numero, f"${h.precio_dia:,.0f}", h.estado))

    def seleccionar_habitacion(self):
        try:
            numero = int(self.campo_numero.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un numero de habitacion valido.", parent=self)
            return
        habitacion = self.hotel.get_habitacion(numero)
        if habitacion is None:
            messagebox.showerror("Error",
                                 f"La habitacion no existe. Debe estar entre 1 y {NUMERO_HABITACIONES}.",
                                 parent=self)
            return
        if habitacion.ocupada:
            messagebox.showerror("Error", f"La habitacion {numero} ya esta ocupada.", parent=self)
            return
        VentanaRegistro(self, habitacion, self.actualizar_tabla)


class VentanaRegistro(tk.Toplevel):
    """Formulario para registrar el ingreso de un huesped."""

    def __init__(self, master, habitacion, al_registrar):
        super().__init__(master)
        self.habitacion = habitacion
        self.al_registrar = al_registrar
        self.title(f"Registro de huesped - Habitacion {habitacion.numero}")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=f"Habitacion {habitacion.numero} - "
                              f"${habitacion.precio_dia:,.0f} por dia").grid(
            row=0, column=0, columnspan=2, pady=(0, 8))

        ttk.Label(frame, text="Fecha de ingreso (aaaa-mm-dd):").grid(row=1, column=0, sticky="w", pady=3)
        self.campo_fecha = ttk.Entry(frame, width=22)
        self.campo_fecha.insert(0, date.today().isoformat())
        self.campo_fecha.grid(row=1, column=1, pady=3)

        ttk.Label(frame, text="Nombre:").grid(row=2, column=0, sticky="w", pady=3)
        self.campo_nombre = ttk.Entry(frame, width=22)
        self.campo_nombre.grid(row=2, column=1, pady=3)

        ttk.Label(frame, text="Apellidos:").grid(row=3, column=0, sticky="w", pady=3)
        self.campo_apellidos = ttk.Entry(frame, width=22)
        self.campo_apellidos.grid(row=3, column=1, pady=3)

        ttk.Label(frame, text="Documento de identidad:").grid(row=4, column=0, sticky="w", pady=3)
        self.campo_documento = ttk.Entry(frame, width=22)
        self.campo_documento.grid(row=4, column=1, pady=3)

        botones = ttk.Frame(frame)
        botones.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(botones, text="Registrar", command=self.registrar).pack(side="left", padx=4)
        ttk.Button(botones, text="Cancelar", command=self.destroy).pack(side="left", padx=4)

    def registrar(self):
        nombre = self.campo_nombre.get().strip()
        apellidos = self.campo_apellidos.get().strip()
        documento = self.campo_documento.get().strip()
        if not nombre or not apellidos or not documento:
            messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=self)
            return
        if not documento.isdigit():
            messagebox.showerror("Error", "El documento de identidad debe contener solo numeros.",
                                 parent=self)
            return
        try:
            fecha = convertir_fecha(self.campo_fecha.get())
        except ValueError:
            messagebox.showerror("Error", "Fecha invalida. Use el formato aaaa-mm-dd.", parent=self)
            return

        self.habitacion.ocupar(Huesped(nombre, apellidos, documento, fecha))
        messagebox.showinfo("Mensaje",
                            f"Registro exitoso de {nombre} {apellidos} "
                            f"en la habitacion {self.habitacion.numero}.", parent=self)
        self.al_registrar()
        self.destroy()


class VentanaSalida(tk.Toplevel):
    """Registra la salida de un huesped: valida fecha, calcula dias y total, y libera la habitacion."""

    def __init__(self, master, hotel):
        super().__init__(master)
        self.hotel = hotel
        self.habitacion = None
        self.fecha_salida = None
        self.title("Salida de huespedes")
        self.resizable(False, False)

        # Parte superior: buscar la habitacion
        norte = ttk.Frame(self, padding=10)
        norte.pack(fill="x")
        ttk.Label(norte, text="Numero de habitacion:").pack(side="left")
        self.campo_numero = ttk.Entry(norte, width=6)
        self.campo_numero.pack(side="left", padx=5)
        ttk.Button(norte, text="Buscar", command=self.buscar_habitacion).pack(side="left")

        # Parte central: datos de la habitacion y de la salida
        centro = ttk.Frame(self, padding=(10, 0, 10, 10))
        centro.pack(fill="both", expand=True)
        self.lbl_habitacion = self._fila(centro, 0, "Habitacion:")
        self.lbl_huesped = self._fila(centro, 1, "Huesped:")
        self.lbl_ingreso = self._fila(centro, 2, "Fecha de ingreso:")

        ttk.Label(centro, text="Fecha de salida (aaaa-mm-dd):").grid(row=3, column=0, sticky="w", pady=3)
        self.campo_salida = ttk.Entry(centro, width=22)
        self.campo_salida.insert(0, date.today().isoformat())
        self.campo_salida.grid(row=3, column=1, sticky="w", pady=3)

        self.lbl_dias = self._fila(centro, 4, "Dias de alojamiento:")
        self.lbl_total = self._fila(centro, 5, "Total a pagar:")

        # Parte inferior: botones
        sur = ttk.Frame(self, padding=10)
        sur.pack(fill="x")
        self.btn_validar = ttk.Button(sur, text="Validar fecha", command=self.validar_fecha)
        self.btn_calcular = ttk.Button(sur, text="Calcular total", command=self.calcular_total)
        self.btn_registrar = ttk.Button(sur, text="Registrar salida", command=self.registrar_salida)
        for btn in (self.btn_validar, self.btn_calcular, self.btn_registrar):
            btn.pack(side="left", padx=4)
        self._habilitar(validar=False, calcular=False, registrar=False)
        self.campo_salida.config(state="disabled")

    @staticmethod
    def _fila(parent, fila, texto):
        ttk.Label(parent, text=texto).grid(row=fila, column=0, sticky="w", pady=3)
        etiqueta = ttk.Label(parent, text="-")
        etiqueta.grid(row=fila, column=1, sticky="w", pady=3)
        return etiqueta

    def _habilitar(self, validar, calcular, registrar):
        self.btn_validar.config(state="normal" if validar else "disabled")
        self.btn_calcular.config(state="normal" if calcular else "disabled")
        self.btn_registrar.config(state="normal" if registrar else "disabled")

    def buscar_habitacion(self):
        try:
            numero = int(self.campo_numero.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un numero de habitacion valido.", parent=self)
            return
        habitacion = self.hotel.get_habitacion(numero)
        if habitacion is None:
            messagebox.showerror("Error",
                                 f"La habitacion no existe. Debe estar entre 1 y {NUMERO_HABITACIONES}.",
                                 parent=self)
            return
        if not habitacion.ocupada:
            messagebox.showerror("Error", f"La habitacion {numero} no esta ocupada.", parent=self)
            return

        self.habitacion = habitacion
        self.fecha_salida = None
        huesped = habitacion.huesped
        self.lbl_habitacion.config(text=str(numero))
        self.lbl_huesped.config(text=f"{huesped.nombre} {huesped.apellidos} (doc. {huesped.documento})")
        self.lbl_ingreso.config(text=huesped.fecha_ingreso.isoformat())
        self.lbl_dias.config(text="-")
        self.lbl_total.config(text="-")
        self.campo_salida.config(state="normal")
        self._habilitar(validar=True, calcular=False, registrar=False)

    def validar_fecha(self):
        self.fecha_salida = None
        self._habilitar(validar=True, calcular=False, registrar=False)
        try:
            salida = convertir_fecha(self.campo_salida.get())
        except ValueError:
            messagebox.showerror("Error", "Fecha invalida. Use el formato aaaa-mm-dd.", parent=self)
            return
        ingreso = self.habitacion.huesped.fecha_ingreso
        if salida <= ingreso:
            messagebox.showerror("Error",
                                 f"La fecha de salida debe ser posterior a la de ingreso ({ingreso}).",
                                 parent=self)
            return
        self.fecha_salida = salida
        self._habilitar(validar=True, calcular=True, registrar=True)
        messagebox.showinfo("Mensaje", "Fecha valida. Ya puede calcular el total.", parent=self)

    def calcular_total(self):
        ingreso = self.habitacion.huesped.fecha_ingreso
        dias = (self.fecha_salida - ingreso).days
        total = dias * self.habitacion.precio_dia
        self.lbl_dias.config(text=str(dias))
        self.lbl_total.config(text=f"${total:,.0f}")

    def registrar_salida(self):
        numero = self.habitacion.numero
        self.habitacion.liberar()
        messagebox.showinfo("Mensaje",
                            f"Salida registrada. La habitacion {numero} queda disponible.",
                            parent=self)
        self.destroy()


class VentanaPrincipalHotel(tk.Tk):
    """Ventana principal con el menu del hotel."""

    def __init__(self):
        super().__init__()
        self.title("Hotel")
        self.geometry("320x150")
        self.resizable(False, False)
        self.hotel = Hotel()

        barra = tk.Menu(self)
        menu = tk.Menu(barra, tearoff=0)
        menu.add_command(label="Consultar habitaciones", command=self.abrir_habitaciones)
        menu.add_command(label="Salida de huespedes", command=self.abrir_salida)
        barra.add_cascade(label="Menu", menu=menu)
        self.config(menu=barra)

        ttk.Label(self, text="Use el menu Menu para comenzar.").pack(expand=True)

    def abrir_habitaciones(self):
        VentanaHabitaciones(self, self.hotel)

    def abrir_salida(self):
        VentanaSalida(self, self.hotel)


if __name__ == "__main__":
    VentanaPrincipalHotel().mainloop()
