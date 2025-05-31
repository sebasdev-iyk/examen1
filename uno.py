import tkinter as tk
from tkinter import ttk, messagebox
class Paciente:
    def __init__(self, nombre, dni, gravedad, tiempo_estimado):
        self.nombre = nombre
        self.dni = dni
        self.gravedad = gravedad  
        self.tiempo_estimado = tiempo_estimado
      class SistemaEmergencia:
    def __init__(self):
        self.cola_pacientes = [] 
        
    def registrar_paciente(self, paciente):
        insertado = False
        for i in range(len(self.cola_pacientes)):
            if paciente.gravedad > self.cola_pacientes[i].gravedad:
                self.cola_pacientes.insert(i, paciente)
                insertado = True
                break
        if not insertado:
            self.cola_pacientes.append(paciente)
    
    def atender_siguiente(self):
        if self.cola_pacientes:
            paciente = self.cola_pacientes.pop(0) 
            return paciente
        return None
    
    def get_pacientes_pendientes(self):
        return self.cola_pacientes.copy()


class InterfazHospital:
    def __init__(self):
        self.sistema = SistemaEmergencia()
        self.root = tk.Tk()
        self.root.title("Sistema de Emergencia Hospitalaria")
        self.root.geometry("700x500")
        self.root.configure(bg='#f0f0f0')
        
        self.crear_interfaz()
        self.actualizar_lista()
        
    def crear_interfaz(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        titulo = tk.Label(main_frame, text="SISTEMA DE EMERGENCIA HOSPITALARIA", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titulo.pack(pady=(0, 20))
        
        self.crear_frame_registro(main_frame)
        
        self.crear_frame_cola(main_frame)
    
        self.crear_boton_atender(main_frame)
        
    def crear_frame_registro(self, parent):
        registro_frame = tk.LabelFrame(parent, text="Registrar Nuevo Paciente", 
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#34495e')
        registro_frame.pack(fill='x', pady=(0, 20))
        campos_frame = tk.Frame(registro_frame, bg='#f0f0f0')
        campos_frame.pack(fill='x', padx=15, pady=15)
    
        tk.Label(campos_frame, text="Nombre:", font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.entry_nombre = tk.Entry(campos_frame, font=('Arial', 10), width=25)
        self.entry_nombre.grid(row=0, column=1, padx=(0, 20))
        
        tk.Label(campos_frame, text="DNI:", font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.entry_dni = tk.Entry(campos_frame, font=('Arial', 10), width=15)
        self.entry_dni.grid(row=0, column=3)
        
        tk.Label(campos_frame, text="Nivel de Emergencia (1-5):", font=('Arial', 10), bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(15, 0))
        self.combo_gravedad = ttk.Combobox(campos_frame, values=[1, 2, 3, 4, 5], width=5, state='readonly')
        self.combo_gravedad.grid(row=1, column=1, sticky='w', pady=(15, 0))
        self.combo_gravedad.set(3)
    
        tk.Label(campos_frame, text="Tiempo estimado (min):", font=('Arial', 10), bg='#f0f0f0').grid(row=1, column=2, sticky='w', padx=(0, 10), pady=(15, 0))
        self.entry_tiempo = tk.Entry(campos_frame, font=('Arial', 10), width=10)
        self.entry_tiempo.grid(row=1, column=3, sticky='w', pady=(15, 0))
        
        btn_registrar = tk.Button(campos_frame, text="Registrar Paciente", 
                                command=self.registrar_paciente, bg='#27ae60', fg='white',
                                font=('Arial', 11, 'bold'), relief='flat', padx=30, pady=8)
        btn_registrar.grid(row=2, column=0, columnspan=4, pady=20)
        
    def crear_frame_cola(self, parent):
        cola_frame = tk.LabelFrame(parent, text="Cola de Pacientes (Orden de Atención)", 
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#e74c3c')
        cola_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        self.tree_cola = ttk.Treeview(cola_frame, columns=('Posición', 'Nombre', 'DNI', 'Gravedad', 'Tiempo Est.'), show='headings', height=12)
        self.tree_cola.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.tree_cola.heading('Posición', text='Posición')
        self.tree_cola.heading('Nombre', text='Nombre')
        self.tree_cola.heading('DNI', text='DNI')
        self.tree_cola.heading('Gravedad', text='Gravedad')
        self.tree_cola.heading('Tiempo Est.', text='Tiempo Est.')
        
        self.tree_cola.column('Posición', width=80)
        self.tree_cola.column('Nombre', width=150)
        self.tree_cola.column('DNI', width=100)
        self.tree_cola.column('Gravedad', width=100)
        self.tree_cola.column('Tiempo Est.', width=100)
        
    def crear_boton_atender(self, parent):
        botones_frame = tk.Frame(parent, bg='#f0f0f0')
        botones_frame.pack(fill='x')
        
        btn_atender = tk.Button(botones_frame, text="ATENDER SIGUIENTE PACIENTE", 
                              command=self.atender_paciente, bg='#e74c3c', fg='white',
                              font=('Arial', 14, 'bold'), relief='flat', padx=40, pady=12)
        btn_atender.pack(side='left')
        
        self.label_proximo = tk.Label(botones_frame, text="", font=('Arial', 12, 'bold'), 
                                    bg='#f0f0f0', fg='#e74c3c')
        self.label_proximo.pack(side='right', padx=(20, 0))
        
    def registrar_paciente(self):
        try:
            nombre = self.entry_nombre.get().strip()
            dni = self.entry_dni.get().strip()
            gravedad = int(self.combo_gravedad.get())
            tiempo_estimado = int(self.entry_tiempo.get())
            
            if not nombre or not dni:
                messagebox.showerror("Error", "Por favor complete el nombre y DNI")
                return
                
            if tiempo_estimado <= 0:
                messagebox.showerror("Error", "El tiempo estimado debe ser mayor a 0")
                return
                
            paciente = Paciente(nombre, dni, gravedad, tiempo_estimado)
            self.sistema.registrar_paciente(paciente)
            
            messagebox.showinfo("Éxito", f"Paciente {nombre} registrado en la cola")
            
            self.entry_nombre.delete(0, tk.END)
            self.entry_dni.delete(0, tk.END)
            self.entry_tiempo.delete(0, tk.END)
            self.combo_gravedad.set(3)
            self.entry_nombre.focus()
            
            self.actualizar_lista()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos")
    
    def atender_paciente(self):
        paciente = self.sistema.atender_siguiente()
        if paciente:
            messagebox.showinfo("Paciente Atendido", 
                              f"Atendiendo a: {paciente.nombre}\n"
                              f"DNI: {paciente.dni}\n"
                              f"Gravedad: Nivel {paciente.gravedad}\n"
                              f"Tiempo estimado: {paciente.tiempo_estimado} min")
            self.actualizar_lista()
        else:
            messagebox.showinfo("Cola Vacía", "No hay pacientes en la cola")
    
    def actualizar_lista(self):
        # Limpiar lista
        for item in self.tree_cola.get_children():
            self.tree_cola.delete(item)
        
        # Actualizar cola de pacientes
        pacientes_cola = self.sistema.get_pacientes_pendientes()
        for i, paciente in enumerate(pacientes_cola, 1):
            # Color diferente para el primer paciente (próximo a atender)
            tag = 'proximo' if i == 1 else ''
            self.tree_cola.insert('', 'end', values=(
                i,
                paciente.nombre,
                paciente.dni,
                f"Nivel {paciente.gravedad}",
                f"{paciente.tiempo_estimado} min"
            ), tags=(tag,))
        
        # Configurar colores
        self.tree_cola.tag_configure('proximo', background='#ffebee')
        
        # Mostrar próximo en cola
        if pacientes_cola:
            proximo = pacientes_cola[0]
            self.label_proximo.config(text=f"PRÓXIMO: {proximo.nombre} (Gravedad {proximo.gravedad})")
        else:
            self.label_proximo.config(text="Cola vacía")
    
    def ejecutar(self):
        self.root.mainloop()
# Ejecutar la aplicación
if __name__ == "__main__":
    app = InterfazHospital()
    app.ejecutar()
