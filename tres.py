import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
import random

class Comando(ABC):
    @abstractmethod
    def ejecutar(self):
        pass
    
    @abstractmethod
    def deshacer(self):
        pass
    
    @abstractmethod
    def obtener_descripcion(self):
        pass

class ComandoDibujar(Comando):
    def __init__(self, canvas, x, y, tipo='rectangulo'):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.tipo = tipo
        self.objeto_id = None
        self.color = f"#{random.randint(0, 0xFFFFFF):06x}"
    
    def ejecutar(self):
        if self.tipo == 'rectangulo':
            self.objeto_id = self.canvas.create_rectangle(
                self.x, self.y, self.x + 80, self.y + 60,
                fill=self.color, outline='black', width=2
            )
        elif self.tipo == 'circulo':
            self.objeto_id = self.canvas.create_oval(
                self.x, self.y, self.x + 60, self.y + 60,
                fill=self.color, outline='black', width=2
            )
        elif self.tipo == 'linea':
            self.objeto_id = self.canvas.create_line(
                self.x, self.y, self.x + 100, self.y + 50,
                fill=self.color, width=3
            )
        return self.objeto_id
    
    def deshacer(self):
        if self.objeto_id:
            self.canvas.delete(self.objeto_id)
    
    def obtener_descripcion(self):
        return f"Dibujar {self.tipo} en ({self.x}, {self.y})"

# Comando para mover un objeto
class ComandoMover(Comando):
    def __init__(self, canvas, objeto_id, dx, dy):
        self.canvas = canvas
        self.objeto_id = objeto_id
        self.dx = dx
        self.dy = dy
    
    def ejecutar(self):
        self.canvas.move(self.objeto_id, self.dx, self.dy)
    
    def deshacer(self):
        self.canvas.move(self.objeto_id, -self.dx, -self.dy)
    
    def obtener_descripcion(self):
        return f"Mover objeto {self.objeto_id} por ({self.dx}, {self.dy})"

class ComandoEliminar(Comando):
    def __init__(self, canvas, objeto_id):
        self.canvas = canvas
        self.objeto_id = objeto_id
        self.coords = None
        self.tipo = None
        self.config = None
        
    def ejecutar(self):
        self.coords = self.canvas.coords(self.objeto_id)
        self.tipo = self.canvas.type(self.objeto_id)
        
        self.config = {}
        if self.tipo:
            try:
                self.config['fill'] = self.canvas.itemcget(self.objeto_id, 'fill')
                self.config['outline'] = self.canvas.itemcget(self.objeto_id, 'outline')
                self.config['width'] = self.canvas.itemcget(self.objeto_id, 'width')
            except:
                pass
        
        self.canvas.delete(self.objeto_id)
    
    def deshacer(self):
        if self.coords and self.tipo:
            if self.tipo == 'rectangle':
                self.objeto_id = self.canvas.create_rectangle(
                    *self.coords,
                    fill=self.config.get('fill', 'gray'),
                    outline=self.config.get('outline', 'black'),
                    width=int(self.config.get('width', 2))
                )
            elif self.tipo == 'oval':
                self.objeto_id = self.canvas.create_oval(
                    *self.coords,
                    fill=self.config.get('fill', 'gray'),
                    outline=self.config.get('outline', 'black'),
                    width=int(self.config.get('width', 2))
                )
            elif self.tipo == 'line':
                self.objeto_id = self.canvas.create_line(
                    *self.coords,
                    fill=self.config.get('fill', 'black'),
                    width=int(self.config.get('width', 3))
                )
    
    def obtener_descripcion(self):
        return f"Eliminar objeto {self.objeto_id}"

class GestorHistorial:
    def __init__(self, limite=10):
        self.pila_deshacer = []  # Pila para deshacer
        self.pila_rehacer = []  # Pila para rehacer
        self.limite = limite
    
    def ejecutar_comando(self, comando):
        comando.ejecutar()
        self.pila_deshacer.append(comando)
        
        # Limitar el tamaño de la pila
        if len(self.pila_deshacer) > self.limite:
            self.pila_deshacer.pop(0)  # Eliminar el comando más antiguo
        
        # Limpiar pila de rehacer al ejecutar un nuevo comando
        self.pila_rehacer.clear()
    
    def deshacer(self):
        if self.pila_deshacer:
            comando = self.pila_deshacer.pop()
            comando.deshacer()
            self.pila_rehacer.append(comando)
            return comando
        return None
    
    def rehacer(self):
        if self.pila_rehacer:
            comando = self.pila_rehacer.pop()
            comando.ejecutar()
            self.pila_deshacer.append(comando)
            return comando
        return None
    
    def puede_deshacer(self):
        return len(self.pila_deshacer) > 0
    
    def puede_rehacer(self):
        return len(self.pila_rehacer) > 0
    
    def obtener_historial_deshacer(self):
        return [cmd.obtener_descripcion() for cmd in reversed(self.pila_deshacer)]
    
    def obtener_historial_rehacer(self):
        return [cmd.obtener_descripcion() for cmd in reversed(self.pila_rehacer)]

# Aplicación principal
class AplicacionDiseno:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Historial de Comandos - Diseño Gráfico")
        self.root.geometry("1000x700")
        
        self.gestor_historial = GestorHistorial(limite=10)
        self.objetos_creados = []
        self.objeto_seleccionado = None
        self.modo_actual = 'dibujar'
        self.tipo_dibujo = 'rectangulo'
        
        self.setup_ui()
        self.actualizar_estado()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Panel de control
        control_frame = ttk.LabelFrame(main_frame, text="Panel de Control", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botones de modo
        ttk.Label(control_frame, text="Modo:").grid(row=0, column=0, padx=5)
        
        self.modo_var = tk.StringVar(value='dibujar')
        ttk.Radiobutton(control_frame, text="[1] Dibujar", variable=self.modo_var, 
                       value='dibujar', command=self.cambiar_modo).grid(row=0, column=1, padx=5)
        ttk.Radiobutton(control_frame, text="[2] Mover", variable=self.modo_var, 
                       value='mover', command=self.cambiar_modo).grid(row=0, column=2, padx=5)
        ttk.Radiobutton(control_frame, text="[3] Eliminar", variable=self.modo_var, 
                       value='eliminar', command=self.cambiar_modo).grid(row=0, column=3, padx=5)
        
        # Separador
        ttk.Separator(control_frame, orient='vertical').grid(row=0, column=4, sticky=(tk.N, tk.S), padx=10)
        
        # Botones deshacer/rehacer
        self.btn_deshacer = ttk.Button(control_frame, text="[4] Deshacer", 
                                      command=self.deshacer, state='disabled')
        self.btn_deshacer.grid(row=0, column=5, padx=5)
        
        self.btn_rehacer = ttk.Button(control_frame, text="[5] Rehacer", 
                                     command=self.rehacer, state='disabled')
        self.btn_rehacer.grid(row=0, column=6, padx=5)
        
        # Opciones de dibujo
        self.frame_opciones = ttk.Frame(control_frame)
        self.frame_opciones.grid(row=1, column=0, columnspan=7, pady=10)
        
        ttk.Label(self.frame_opciones, text="Tipo de objeto:").pack(side=tk.LEFT, padx=5)
        self.tipo_var = tk.StringVar(value='rectangulo')
        ttk.Radiobutton(self.frame_opciones, text="Rectángulo", 
                       variable=self.tipo_var, value='rectangulo').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.frame_opciones, text="Círculo", 
                       variable=self.tipo_var, value='circulo').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.frame_opciones, text="Línea", 
                       variable=self.tipo_var, value='linea').pack(side=tk.LEFT, padx=5)
        
        # Canvas para dibujar
        canvas_frame = ttk.LabelFrame(main_frame, text="Área de Diseño", padding="5")
        canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Eventos del canvas
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)
        
        # Panel de historial
        historial_frame = ttk.LabelFrame(main_frame, text="Historial", padding="10")
        historial_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        historial_frame.rowconfigure(1, weight=1)
        historial_frame.rowconfigure(3, weight=1)
        
        # Pila de deshacer
        ttk.Label(historial_frame, text="Pila Deshacer:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        
        self.lista_deshacer = tk.Listbox(historial_frame, height=8, width=30)
        self.lista_deshacer.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Pila de rehacer
        ttk.Label(historial_frame, text="Pila Rehacer:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        
        self.lista_rehacer = tk.Listbox(historial_frame, height=8, width=30)
        self.lista_rehacer.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Información
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.label_info = ttk.Label(info_frame, text="Haga clic en el canvas para realizar acciones")
        self.label_info.pack()
        
        ttk.Button(info_frame, text="Limpiar Todo", command=self.limpiar_todo).pack(side=tk.LEFT, padx=5)
        ttk.Button(info_frame, text="Información del Sistema", command=self.mostrar_info).pack(side=tk.LEFT, padx=5)
        
        # Atajos de teclado
        self.root.bind('1', lambda e: self.modo_var.set('dibujar') or self.cambiar_modo())
        self.root.bind('2', lambda e: self.modo_var.set('mover') or self.cambiar_modo())
        self.root.bind('3', lambda e: self.modo_var.set('eliminar') or self.cambiar_modo())
        self.root.bind('4', lambda e: self.deshacer())
        self.root.bind('5', lambda e: self.rehacer())
        self.root.bind('<Control-z>', lambda e: self.deshacer())
        self.root.bind('<Control-y>', lambda e: self.rehacer())
    
    def cambiar_modo(self):
        self.modo_actual = self.modo_var.get()
        self.objeto_seleccionado = None
        self.canvas.delete("seleccion")
        
        if self.modo_actual == 'dibujar':
            self.frame_opciones.pack()
            self.label_info.config(text="Haga clic para dibujar un objeto")
        elif self.modo_actual == 'mover':
            self.frame_opciones.pack_forget()
            self.label_info.config(text="Haga clic y arrastre un objeto para moverlo")
        elif self.modo_actual == 'eliminar':
            self.frame_opciones.pack_forget()
            self.label_info.config(text="Haga clic en un objeto para eliminarlo")
    
    def canvas_click(self, event):
        if self.modo_actual == 'dibujar':
            self.dibujar_objeto(event.x, event.y)
        elif self.modo_actual == 'mover':
            self.iniciar_movimiento(event)
        elif self.modo_actual == 'eliminar':
            self.eliminar_objeto(event)
    
    def dibujar_objeto(self, x, y):
        tipo = self.tipo_var.get()
        comando = ComandoDibujar(self.canvas, x, y, tipo)
        objeto_id = self.gestor_historial.ejecutar_comando(comando)
        self.objetos_creados.append(objeto_id)
        self.actualizar_estado()
        self.label_info.config(text=f"Objeto {tipo} dibujado en ({x}, {y})")
    
    def iniciar_movimiento(self, event):
        # Encontrar objeto más cercano
        self.objeto_seleccionado = self.canvas.find_closest(event.x, event.y)[0]
        if self.objeto_seleccionado:
            # Resaltar objeto seleccionado
            bbox = self.canvas.bbox(self.objeto_seleccionado)
            if bbox:
                self.canvas.create_rectangle(
                    bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2,
                    outline='red', width=2, tags="seleccion"
                )
            self.start_x = event.x
            self.start_y = event.y
    
    def canvas_drag(self, event):
        if self.modo_actual == 'mover' and self.objeto_seleccionado:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.objeto_seleccionado, dx, dy)
            self.canvas.move("seleccion", dx, dy)
            self.start_x = event.x
            self.start_y = event.y
    
    def canvas_release(self, event):
        if self.modo_actual == 'mover' and self.objeto_seleccionado:
            # Calcular desplazamiento total
            coords_inicial = self.canvas.coords(self.objeto_seleccionado)
            if coords_inicial:
                # Registrar el movimiento como comando
                bbox = self.canvas.bbox(self.objeto_seleccionado)
                dx = event.x - self.start_x
                dy = event.y - self.start_y
                
                if dx != 0 or dy != 0:
                    comando = ComandoMover(self.canvas, self.objeto_seleccionado, dx, dy)
                    self.gestor_historial.ejecutar_comando(comando)
                    self.actualizar_estado()
                    self.label_info.config(text=f"Objeto {self.objeto_seleccionado} movido")
            
            self.canvas.delete("seleccion")
            self.objeto_seleccionado = None
    
    def eliminar_objeto(self, event):
        objeto = self.canvas.find_closest(event.x, event.y)[0]
        if objeto:
            comando = ComandoEliminar(self.canvas, objeto)
            self.gestor_historial.ejecutar_comando(comando)
            if objeto in self.objetos_creados:
                self.objetos_creados.remove(objeto)
            self.actualizar_estado()
            self.label_info.config(text=f"Objeto {objeto} eliminado")
    
    def deshacer(self):
        comando = self.gestor_historial.deshacer()
        if comando:
            self.actualizar_estado()
            self.label_info.config(text=f"Deshecho: {comando.obtener_descripcion()}")
        else:
            self.label_info.config(text="No hay acciones para deshacer")
    
    def rehacer(self):
        comando = self.gestor_historial.rehacer()
        if comando:
            self.actualizar_estado()
            self.label_info.config(text=f"Rehecho: {comando.obtener_descripcion()}")
        else:
            self.label_info.config(text="No hay acciones para rehacer")
    
    def actualizar_estado(self):
        # Actualizar botones
        self.btn_deshacer.config(state='normal' if self.gestor_historial.puede_deshacer() else 'disabled')
        self.btn_rehacer.config(state='normal' if self.gestor_historial.puede_rehacer() else 'disabled')
        
        # Actualizar listas de historial
        self.lista_deshacer.delete(0, tk.END)
        for desc in self.gestor_historial.obtener_historial_deshacer():
            self.lista_deshacer.insert(0, desc)
        
        self.lista_rehacer.delete(0, tk.END)
        for desc in self.gestor_historial.obtener_historial_rehacer():
            self.lista_rehacer.insert(0, desc)
    
    def limpiar_todo(self):
        if messagebox.askyesno("Confirmar", "¿Desea limpiar todo el canvas y el historial?"):
            self.canvas.delete("all")
            self.gestor_historial = GestorHistorial(limite=10)
            self.objetos_creados.clear()
            self.actualizar_estado()
            self.label_info.config(text="Canvas y historial limpiados")
    
    def mostrar_info(self):
        info = """
SISTEMA DE HISTORIAL DE COMANDOS

1. ESTRUCTURA DE DATOS UTILIZADA:
   • PILAS (Stacks) - Estructura LIFO (Last In, First Out)
   • Pila de Deshacer: Almacena comandos ejecutados
   • Pila de Rehacer: Almacena comandos deshechos
   
2. JUSTIFICACIÓN DE LAS PILAS:
   • Orden natural: La última acción es la primera en deshacerse
   • Eficiencia O(1): Push y pop son operaciones constantes
   • Gestión simple: No requiere índices ni búsquedas
   • Patrón Command: Cada acción es un objeto con ejecutar/deshacer

3. MANEJO DE REVERSIÓN:
   • Deshacer: Pop de pila_deshacer → ejecutar deshacer() → push a pila_rehacer
   • Rehacer: Pop de pila_rehacer → ejecutar ejecutar() → push a pila_deshacer
   • Nueva acción: Limpia pila_rehacer (comportamiento estándar)

4. OPTIMIZACIÓN DE MEMORIA:
   • Límite de 10 acciones por pila
   • FIFO para eliminar: Se descarta la acción más antigua
   • Evita crecimiento ilimitado de memoria

5. ATAJOS DE TECLADO:
   • 1-5: Acceso rápido a opciones del menú
   • Ctrl+Z: Deshacer
   • Ctrl+Y: Rehacer

6. PATRÓN DE DISEÑO:
   • Command Pattern: Encapsula acciones como objetos
   • Permite parametrizar, encolar y deshacer operaciones
   • Separación entre invocador y receptor
"""
        
        ventana_info = tk.Toplevel(self.root)
        ventana_info.title("Información del Sistema")
        ventana_info.geometry("600x550")
        
        text_widget = tk.Text(ventana_info, wrap=tk.WORD, width=70, height=30)
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, info)
        text_widget.config(state='disabled')
        
        ttk.Button(ventana_info, text="Cerrar", command=ventana_info.destroy).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionDiseno(root)
    root.mainloop()
