"""
Ejercicio 8.4 - Calculo de la nomina de una empresa (interfaz grafica con tkinter).

Menu:
  - Agregar empleado: formulario con los datos del empleado.
  - Calcular nomina: tabla con nombre, apellidos y sueldo mensual, y total abajo.
  - Guardar archivo: crea Nomina.txt en la carpeta elegida.

Ejecutar:  python ejercicio_8_4_nomina.py
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

CARGOS = ["Directivo", "Estrategico", "Operativo"]
GENEROS = ["Masculino", "Femenino"]


# ----------------------------------------------------------------------
# Modelo
# ----------------------------------------------------------------------
class Empleado:
    """Empleado de la empresa con sus datos de nomina."""

    def __init__(self, nombre, apellidos, cargo, genero, salario_dia,
                 dias_trabajados, otros_ingresos, pagos_salud, aporte_pensiones):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pensiones = aporte_pensiones

    def calcular_nomina(self):
        """Salario mensual = (dias * salario por dia) + otros ingresos - salud - pensiones."""
        return (self.dias_trabajados * self.salario_dia
                + self.otros_ingresos
                - self.pagos_salud
                - self.aporte_pensiones)


class ListaEmpleados:
    """Guarda los empleados y calcula la nomina total."""

    def __init__(self):
        self.empleados = []

    def agregar(self, empleado):
        self.empleados.append(empleado)

    def esta_vacia(self):
        return len(self.empleados) == 0

    def total_nomina(self):
        return sum(e.calcular_nomina() for e in self.empleados)

    def convertir_texto(self):
        """Texto con los datos de cada empleado y el total (para Nomina.txt)."""
        lineas = []
        for e in self.empleados:
            lineas.append(f"Nombre = {e.nombre}")
            lineas.append(f"Apellidos = {e.apellidos}")
            lineas.append(f"Cargo = {e.cargo}")
            lineas.append(f"Genero = {e.genero}")
            lineas.append(f"Salario por dia = ${e.salario_dia:,.2f}")
            lineas.append(f"Dias trabajados = {e.dias_trabajados}")
            lineas.append(f"Otros ingresos = ${e.otros_ingresos:,.2f}")
            lineas.append(f"Pagos salud = ${e.pagos_salud:,.2f}")
            lineas.append(f"Aporte pensiones = ${e.aporte_pensiones:,.2f}")
            lineas.append(f"Salario mensual = ${e.calcular_nomina():,.2f}")
            lineas.append("---------")
        lineas.append(f"Total nomina = ${self.total_nomina():,.2f}")
        return "\n".join(lineas)


# ----------------------------------------------------------------------
# Interfaz grafica
# ----------------------------------------------------------------------
def leer_numero(texto, nombre_campo):
    """Convierte el texto a float. Lanza ValueError si no es valido o es negativo."""
    try:
        valor = float(texto.strip())
    except ValueError:
        raise ValueError(f"{nombre_campo} debe ser un numero valido.")
    if valor < 0:
        raise ValueError(f"{nombre_campo} no puede ser negativo.")
    return valor


class VentanaAgregarEmpleado(tk.Toplevel):
    """Formulario para ingresar los datos de un empleado."""

    def __init__(self, master, lista):
        super().__init__(master)
        self.lista = lista
        self.title("Agregar Empleado")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        # Nombre y apellidos
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=3)
        self.campo_nombre = ttk.Entry(frame, width=25)
        self.campo_nombre.grid(row=0, column=1, pady=3)

        ttk.Label(frame, text="Apellidos:").grid(row=1, column=0, sticky="w", pady=3)
        self.campo_apellidos = ttk.Entry(frame, width=25)
        self.campo_apellidos.grid(row=1, column=1, pady=3)

        # Cargo (lista desplegable)
        ttk.Label(frame, text="Cargo:").grid(row=2, column=0, sticky="w", pady=3)
        self.campo_cargo = ttk.Combobox(frame, values=CARGOS, state="readonly", width=23)
        self.campo_cargo.current(0)
        self.campo_cargo.grid(row=2, column=1, pady=3)

        # Genero (botones de radio)
        ttk.Label(frame, text="Genero:").grid(row=3, column=0, sticky="w", pady=3)
        self.genero_var = tk.StringVar(value="Masculino")
        frame_genero = ttk.Frame(frame)
        frame_genero.grid(row=3, column=1, sticky="w", pady=3)
        for g in GENEROS:
            ttk.Radiobutton(frame_genero, text=g, value=g,
                            variable=self.genero_var).pack(side="left", padx=2)

        # Salario por dia
        ttk.Label(frame, text="Salario por dia:").grid(row=4, column=0, sticky="w", pady=3)
        self.campo_salario = ttk.Entry(frame, width=25)
        self.campo_salario.grid(row=4, column=1, pady=3)

        # Dias trabajados (1 a 31)
        ttk.Label(frame, text="Dias trabajados:").grid(row=5, column=0, sticky="w", pady=3)
        self.campo_dias = tk.Spinbox(frame, from_=1, to=31, width=10)
        self.campo_dias.delete(0, "end")
        self.campo_dias.insert(0, "1")
        self.campo_dias.grid(row=5, column=1, sticky="w", pady=3)

        # Otros ingresos, salud y pensiones
        ttk.Label(frame, text="Otros ingresos:").grid(row=6, column=0, sticky="w", pady=3)
        self.campo_otros = ttk.Entry(frame, width=25)
        self.campo_otros.insert(0, "0")
        self.campo_otros.grid(row=6, column=1, pady=3)

        ttk.Label(frame, text="Pagos salud:").grid(row=7, column=0, sticky="w", pady=3)
        self.campo_salud = ttk.Entry(frame, width=25)
        self.campo_salud.insert(0, "0")
        self.campo_salud.grid(row=7, column=1, pady=3)

        ttk.Label(frame, text="Aporte pensiones:").grid(row=8, column=0, sticky="w", pady=3)
        self.campo_pensiones = ttk.Entry(frame, width=25)
        self.campo_pensiones.insert(0, "0")
        self.campo_pensiones.grid(row=8, column=1, pady=3)

        # Botones
        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=9, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(frame_botones, text="Agregar", command=self.agregar_empleado).pack(side="left", padx=4)
        ttk.Button(frame_botones, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=4)
        ttk.Button(frame_botones, text="Cerrar", command=self.destroy).pack(side="left", padx=4)

    def agregar_empleado(self):
        nombre = self.campo_nombre.get().strip()
        apellidos = self.campo_apellidos.get().strip()
        if not nombre or not apellidos:
            messagebox.showerror("Error", "Nombre y apellidos son obligatorios.", parent=self)
            return
        try:
            salario = leer_numero(self.campo_salario.get(), "Salario por dia")
            otros = leer_numero(self.campo_otros.get(), "Otros ingresos")
            salud = leer_numero(self.campo_salud.get(), "Pagos por salud")
            pensiones = leer_numero(self.campo_pensiones.get(), "Aporte pensiones")
            dias = int(self.campo_dias.get())
            if not 1 <= dias <= 31:
                raise ValueError("Los dias trabajados deben estar entre 1 y 31.")
        except ValueError as ex:
            messagebox.showerror("Error", str(ex), parent=self)
            return

        self.lista.agregar(Empleado(nombre, apellidos, self.campo_cargo.get(),
                                    self.genero_var.get(), salario, dias,
                                    otros, salud, pensiones))
        messagebox.showinfo("Mensaje", "Empleado agregado correctamente.", parent=self)
        self.limpiar_campos()

    def limpiar_campos(self):
        self.campo_nombre.delete(0, "end")
        self.campo_apellidos.delete(0, "end")
        self.campo_cargo.current(0)
        self.genero_var.set("Masculino")
        self.campo_salario.delete(0, "end")
        self.campo_dias.delete(0, "end")
        self.campo_dias.insert(0, "1")
        self.campo_otros.delete(0, "end")
        self.campo_otros.insert(0, "0")
        self.campo_salud.delete(0, "end")
        self.campo_salud.insert(0, "0")
        self.campo_pensiones.delete(0, "end")
        self.campo_pensiones.insert(0, "0")


class VentanaNomina(tk.Toplevel):
    """Tabla con los empleados y su sueldo mensual, y el total de la nomina."""

    def __init__(self, master, lista):
        super().__init__(master)
        self.title("Calcular Nomina")
        self.geometry("480x300")

        tabla = ttk.Treeview(self, columns=("nombre", "apellidos", "sueldo"), show="headings")
        tabla.heading("nombre", text="Nombre")
        tabla.heading("apellidos", text="Apellidos")
        tabla.heading("sueldo", text="Sueldo mensual")
        tabla.column("sueldo", anchor="e")
        for e in lista.empleados:
            tabla.insert("", "end", values=(e.nombre, e.apellidos,
                                            f"${e.calcular_nomina():,.2f}"))
        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        total = tk.Label(self, text=f"Total nomina de la empresa: ${lista.total_nomina():,.2f}",
                         font=("Arial", 11, "bold"))
        total.pack(pady=(0, 10))


class VentanaPrincipal(tk.Tk):
    """Ventana principal con la barra de menus."""

    def __init__(self):
        super().__init__()
        self.title("Nomina")
        self.geometry("300x150")
        self.resizable(False, False)
        self.lista = ListaEmpleados()

        barra = tk.Menu(self)
        menu = tk.Menu(barra, tearoff=0)
        menu.add_command(label="Agregar empleado", command=self.abrir_agregar)
        menu.add_command(label="Calcular nomina", command=self.abrir_nomina)
        menu.add_separator()
        menu.add_command(label="Guardar archivo", command=self.guardar_archivo)
        barra.add_cascade(label="Menu", menu=menu)
        self.config(menu=barra)

        ttk.Label(self, text="Use el menu Menu para comenzar.").pack(expand=True)

    def abrir_agregar(self):
        VentanaAgregarEmpleado(self, self.lista)

    def abrir_nomina(self):
        VentanaNomina(self, self.lista)

    def guardar_archivo(self):
        if self.lista.esta_vacia():
            messagebox.showwarning("Aviso", "No hay empleados registrados.", parent=self)
            return
        carpeta = filedialog.askdirectory(title="Seleccione la carpeta para Nomina.txt")
        if not carpeta:
            return
        ruta = os.path.join(carpeta, "Nomina.txt")
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(self.lista.convertir_texto())
            messagebox.showinfo("Mensaje", f"El archivo Nomina.txt se creo en:\n{ruta}",
                                parent=self)
        except OSError as ex:
            messagebox.showerror("Error", f"Error al guardar: {ex}", parent=self)


if __name__ == "__main__":
    VentanaPrincipal().mainloop()
