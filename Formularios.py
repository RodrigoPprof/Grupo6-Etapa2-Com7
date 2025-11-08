import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class FormularioTarea(tk.Toplevel): # Toplevel crea una nueva ventana separada del main.
    def __init__(self, master, db, tarea=None):
        super().__init__(master)
        self.db = db
        self.tarea = tarea
        self.title("✏️ Editar Tarea" if tarea else "➕ Nueva Tarea") #Cambia el título según si se está editando o creando
        self.geometry("420x440")
        self.config(bg="#f2faff")
        self.crear_widgets() #Crea los elementos gráficos.

    # Creamos una ventana flotante
    def crear_widgets(self):
        tk.Label(self, text="Título:", bg="#f2faff").pack(pady=5)
        self.titulo = tk.Entry(self, width=40)
        self.titulo.pack(pady=5)

        tk.Label(self, text="Descripción:", bg="#f2faff").pack(pady=5)
        self.descripcion = tk.Entry(self, width=40)
        self.descripcion.pack(pady=5)

        tk.Label(self, text="Fecha:", bg="#f2faff").pack(pady=5)
        self.fecha = DateEntry(self, width=37, background="lightblue", date_pattern="yyyy-mm-dd")
        self.fecha.pack(pady=5)

        hora_frame = ttk.Frame(self)
        hora_frame.pack(pady=5)
        tk.Label(hora_frame, text="Hora:", bg="#f2faff").grid(row=0, column=0, padx=5)
        self.hora = tk.Spinbox(hora_frame, from_=0, to=23, width=5, format="%02.0f")
        self.minuto = tk.Spinbox(hora_frame, from_=0, to=59, width=5, format="%02.0f")
        self.hora.grid(row=0, column=1)
        tk.Label(hora_frame, text="Minutos:", bg="#f2faff").grid(row=0, column=2, padx=5)
        self.minuto.grid(row=0, column=3)

        tk.Label(self, text="Notas:", bg="#f2faff").pack(pady=5)
        self.notas = tk.Entry(self, width=40)
        self.notas.pack(pady=5)

        tk.Label(self, text="Categoría:", bg="#f2faff").pack(pady=5)
        categorias = [c[1] for c in self.db.listar_categorias()]
        # Menú desplegable con las categorías desde la base
        self.categoria = ttk.Combobox(self, values=categorias, state="readonly", width=37)
        self.categoria.set(categorias[0])
        self.categoria.pack(pady=5)

        ttk.Button(self, text="Guardar", command=self.guardar).pack(pady=15)

        if self.tarea:
            self.cargar_datos()


    def cargar_datos(self):
        t = self.tarea
        self.titulo.insert(0, t[1])
        self.descripcion.insert(0, t[2])
        self.notas.insert(0, t[4])
        fecha_str, hora_str = t[3].split(" ")
        self.fecha.set_date(datetime.strptime(fecha_str, "%Y-%m-%d"))
        h, m = hora_str.split(":")
        self.hora.delete(0, tk.END)
        self.hora.insert(0, h)
        self.minuto.delete(0, tk.END)
        self.minuto.insert(0, m)
        if t[6]:
            self.categoria.set(t[6])

    # Verificamos que no esté vacío el campo título
    def guardar(self):
        titulo = self.titulo.get().strip()
        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio.")
            return

        #Combina fecha y hora en formato YYYY-MM-DD HH:MM
        fecha = self.fecha.get_date().strftime("%Y-%m-%d")
        hora = self.hora.get()
        minuto = self.minuto.get()
        fecha_hora = f"{fecha} {hora}:{minuto}"
        cat_nombre = self.categoria.get()

        # Buscar id de categoría
        for c in self.db.listar_categorias():
            if c[1] == cat_nombre:
                categoria_id = c[0]
                break

        if self.tarea:
            self.db.actualizar_tarea(self.tarea[0], titulo, self.descripcion.get(), fecha_hora, self.notas.get(), categoria_id)
        else:
            self.db.agregar_tarea(titulo, self.descripcion.get(), fecha_hora, self.notas.get(), categoria_id)

        messagebox.showinfo("Éxito", "Tarea guardada correctamente.")
        self.destroy()
