import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class GrafoRutas:
    def __init__(self):
        self.nombre_a_indice = {}
        self.indice_a_nombre = {}
        self.matriz = []
        self.num_puntos = 0
    
    def _obtener_indice(self, punto):
        if punto not in self.nombre_a_indice:
            self.nombre_a_indice[punto] = self.num_puntos
            self.indice_a_nombre[self.num_puntos] = punto
            self.num_puntos += 1
            
            self.matriz.append([0] * self.num_puntos)
            for i in range(self.num_puntos - 1):
                self.matriz[i].append(0)
        
        return self.nombre_a_indice[punto]
    
    def agregar_conexion(self, punto1, punto2):
        idx1 = self._obtener_indice(punto1)
        idx2 = self._obtener_indice(punto2)
        
        self.matriz[idx1][idx2] = 1
        self.matriz[idx2][idx1] = 1
    
    def eliminar_conexion(self, punto1, punto2):
        if punto1 in self.nombre_a_indice and punto2 in self.nombre_a_indice:
            idx1 = self.nombre_a_indice[punto1]
            idx2 = self.nombre_a_indice[punto2]
            self.matriz[idx1][idx2] = 0
            self.matriz[idx2][idx1] = 0
    
    def obtener_vecinos(self, punto):
        if punto not in self.nombre_a_indice:
            return []
        
        idx = self.nombre_a_indice[punto]
        vecinos = []
        
        for i in range(self.num_puntos):
            if self.matriz[idx][i] == 1:
                vecinos.append(self.indice_a_nombre[i])
        
        return vecinos
    
    def existe_camino_dfs(self, inicio, fin):
        if inicio not in self.nombre_a_indice or fin not in self.nombre_a_indice:
            return False
        
        visitados = [False] * self.num_puntos
        pila = [self.nombre_a_indice[inicio]]
        
        while pila:
            idx_actual = pila.pop()
            
            if self.indice_a_nombre[idx_actual] == fin:
                return True
            
            if not visitados[idx_actual]:
                visitados[idx_actual] = True
                
                # Agregar vecinos no visitados
                for i in range(self.num_puntos):
                    if self.matriz[idx_actual][i] == 1 and not visitados[i]:
                        pila.append(i)
        
        return False
    
    def existe_camino_bfs(self, inicio, fin):
        if inicio not in self.nombre_a_indice or fin not in self.nombre_a_indice:
            return False
        
        visitados = [False] * self.num_puntos
        cola = []  # Usamos lista en lugar de deque
        
        idx_inicio = self.nombre_a_indice[inicio]
        cola.append(idx_inicio)
        visitados[idx_inicio] = True
        
        while cola:
            idx_actual = cola.pop(0)  # pop(0) para comportamiento FIFO
            
            if self.indice_a_nombre[idx_actual] == fin:
                return True
            
            # Agregar vecinos no visitados
            for i in range(self.num_puntos):
                if self.matriz[idx_actual][i] == 1 and not visitados[i]:
                    visitados[i] = True
                    cola.append(i)
        
        return False
    
    def encontrar_todas_rutas(self, inicio, fin, ruta=None, rutas=None):
        if ruta is None:
            ruta = []
        if rutas is None:
            rutas = []
        
        if inicio not in self.nombre_a_indice or fin not in self.nombre_a_indice:
            return rutas
        
        ruta = ruta + [inicio]
        
        if inicio == fin:
            rutas.append(ruta)
            return rutas
        
        # Obtener vecinos y explorar recursivamente
        vecinos = self.obtener_vecinos(inicio)
        for vecino in vecinos:
            if vecino not in ruta:  # Evitar ciclos
                self.encontrar_todas_rutas(vecino, fin, ruta, rutas)
        
        return rutas
    
    def obtener_camino_mas_corto_bfs(self, inicio, fin):
        """Encuentra el camino más corto usando BFS"""
        if inicio not in self.nombre_a_indice or fin not in self.nombre_a_indice:
            return None
        
        visitados = [False] * self.num_puntos
        cola = []  # Lista como cola
        padre = {}  # Para reconstruir el camino
        
        idx_inicio = self.nombre_a_indice[inicio]
        cola.append(idx_inicio)
        visitados[idx_inicio] = True
        padre[idx_inicio] = None
        
        encontrado = False
        idx_fin = self.nombre_a_indice[fin]
        
        while cola and not encontrado:
            idx_actual = cola.pop(0)
            
            if idx_actual == idx_fin:
                encontrado = True
                break
            
            # Explorar vecinos
            for i in range(self.num_puntos):
                if self.matriz[idx_actual][i] == 1 and not visitados[i]:
                    visitados[i] = True
                    padre[i] = idx_actual
                    cola.append(i)
        
        if not encontrado:
            return None
    
        camino = []
        idx_actual = idx_fin
        while idx_actual is not None:
            camino.append(self.indice_a_nombre[idx_actual])
            idx_actual = padre.get(idx_actual)
        
        camino.reverse()
        return camino
    
    def obtener_puntos(self):
        return set(self.nombre_a_indice.keys())
    
    def obtener_conexiones_dict(self):
        conexiones = {}
        for i in range(self.num_puntos):
            punto = self.indice_a_nombre[i]
            vecinos = []
            for j in range(self.num_puntos):
                if self.matriz[i][j] == 1:
                    vecinos.append(self.indice_a_nombre[j])
            if vecinos:
                conexiones[punto] = vecinos
        return conexiones

class AplicacionRutas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Análisis de Rutas - Ciudad Altiplánica")
        self.root.geometry("1200x700")
        
        self.grafo = GrafoRutas()
        self.setup_ui()
        self.cargar_ejemplo()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # === Sección de entrada de datos ===
        ttk.Label(main_frame, text="ENTRADA DE DATOS", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=3, pady=5)
        
        # Agregar conexión
        ttk.Label(main_frame, text="Punto 1:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.punto1_entry = ttk.Entry(main_frame, width=20)
        self.punto1_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(main_frame, text="Punto 2:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.punto2_entry = ttk.Entry(main_frame, width=20)
        self.punto2_entry.grid(row=2, column=1, padx=5)
        
        # Botones de conexión
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=1, column=2, rowspan=2, padx=10)
        
        ttk.Button(btn_frame, text="Agregar Conexión", command=self.agregar_conexion).pack(pady=2)
        ttk.Button(btn_frame, text="Eliminar Conexión", command=self.eliminar_conexion).pack(pady=2)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # === Sección de búsqueda ===
        ttk.Label(main_frame, text="BÚSQUEDA DE RUTAS", font=('Arial', 12, 'bold')).grid(row=4, column=0, columnspan=3, pady=5)
        
        # Búsqueda de rutas
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=5, column=0, columnspan=3, pady=5)
        
        ttk.Label(search_frame, text="Desde:").pack(side=tk.LEFT, padx=5)
        self.desde_entry = ttk.Entry(search_frame, width=15)
        self.desde_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Hasta:").pack(side=tk.LEFT, padx=5)
        self.hasta_entry = ttk.Entry(search_frame, width=15)
        self.hasta_entry.pack(side=tk.LEFT, padx=5)
        
        # Botones de búsqueda
        search_btn_frame = ttk.Frame(main_frame)
        search_btn_frame.grid(row=6, column=0, columnspan=3, pady=5)
        
        ttk.Button(search_btn_frame, text="Verificar con DFS", command=self.verificar_dfs).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_btn_frame, text="Verificar con BFS", command=self.verificar_bfs).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_btn_frame, text="Mostrar Todas las Rutas", command=self.mostrar_todas_rutas).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_btn_frame, text="Ruta Más Corta (BFS)", command=self.mostrar_ruta_mas_corta).pack(side=tk.LEFT, padx=5)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # === Visualización ===
        vis_frame = ttk.Frame(main_frame)
        vis_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        vis_frame.columnconfigure(0, weight=1)
        vis_frame.columnconfigure(1, weight=2)
        vis_frame.rowconfigure(1, weight=1)
        
        # Lista de conexiones
        ttk.Label(vis_frame, text="CONEXIONES ACTUALES", font=('Arial', 10, 'bold')).grid(row=0, column=0, pady=5)
        
        self.conexiones_text = scrolledtext.ScrolledText(vis_frame, width=40, height=15)
        self.conexiones_text.grid(row=1, column=0, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Resultados
        ttk.Label(vis_frame, text="RESULTADOS", font=('Arial', 10, 'bold')).grid(row=0, column=1, pady=5)
        
        self.resultados_text = scrolledtext.ScrolledText(vis_frame, width=60, height=15)
        self.resultados_text.grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones adicionales
        extra_btn_frame = ttk.Frame(main_frame)
        extra_btn_frame.grid(row=9, column=0, columnspan=3, pady=10)
        
        ttk.Button(extra_btn_frame, text="Limpiar Grafo", command=self.limpiar_grafo).pack(side=tk.LEFT, padx=5)
        ttk.Button(extra_btn_frame, text="Cargar Ejemplo", command=self.cargar_ejemplo).pack(side=tk.LEFT, padx=5)
        ttk.Button(extra_btn_frame, text="Ver Matriz", command=self.mostrar_matriz).pack(side=tk.LEFT, padx=5)
        ttk.Button(extra_btn_frame, text="Información del Sistema", command=self.mostrar_info).pack(side=tk.LEFT, padx=5)
    
    def agregar_conexion(self):
        punto1 = self.punto1_entry.get().strip()
        punto2 = self.punto2_entry.get().strip()
        
        if not punto1 or not punto2:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambos puntos")
            return
        
        if punto1 == punto2:
            messagebox.showwarning("Advertencia", "Los puntos deben ser diferentes")
            return
        
        self.grafo.agregar_conexion(punto1, punto2)
        self.actualizar_conexiones()
        self.punto1_entry.delete(0, tk.END)
        self.punto2_entry.delete(0, tk.END)
        
        messagebox.showinfo("Éxito", f"Conexión agregada: {punto1} <-> {punto2}")
    
    def eliminar_conexion(self):
        punto1 = self.punto1_entry.get().strip()
        punto2 = self.punto2_entry.get().strip()
        
        if not punto1 or not punto2:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambos puntos")
            return
        
        self.grafo.eliminar_conexion(punto1, punto2)
        self.actualizar_conexiones()
        self.punto1_entry.delete(0, tk.END)
        self.punto2_entry.delete(0, tk.END)
        
        messagebox.showinfo("Éxito", f"Conexión eliminada: {punto1} <-> {punto2}")
    
    def actualizar_conexiones(self):
        self.conexiones_text.delete(1.0, tk.END)
        
        puntos = self.grafo.obtener_puntos()
        if not puntos:
            self.conexiones_text.insert(tk.END, "No hay conexiones registradas")
            return
        
        self.conexiones_text.insert(tk.END, f"Puntos totales: {len(puntos)}\n")
        self.conexiones_text.insert(tk.END, f"Puntos: {', '.join(sorted(puntos))}\n\n")
        
        conexiones = self.grafo.obtener_conexiones_dict()
        for punto in sorted(conexiones.keys()):
            vecinos = ', '.join(sorted(conexiones[punto]))
            self.conexiones_text.insert(tk.END, f"{punto} -> {vecinos}\n")
    
    def verificar_dfs(self):
        desde = self.desde_entry.get().strip()
        hasta = self.hasta_entry.get().strip()
        
        if not desde or not hasta:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambos puntos")
            return
        
        existe = self.grafo.existe_camino_dfs(desde, hasta)
        
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, "=== VERIFICACIÓN CON DFS ===\n\n")
        self.resultados_text.insert(tk.END, f"Desde: {desde}\n")
        self.resultados_text.insert(tk.END, f"Hasta: {hasta}\n\n")
        
        if existe:
            self.resultados_text.insert(tk.END, "✓ SÍ existe un camino entre los puntos\n", 'success')
            self.resultados_text.tag_config('success', foreground='green')
        else:
            self.resultados_text.insert(tk.END, "✗ NO existe un camino entre los puntos\n", 'error')
            self.resultados_text.tag_config('error', foreground='red')
    
    def verificar_bfs(self):
        desde = self.desde_entry.get().strip()
        hasta = self.hasta_entry.get().strip()
        
        if not desde or not hasta:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambos puntos")
            return
        
        existe = self.grafo.existe_camino_bfs(desde, hasta)
        
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, "=== VERIFICACIÓN CON BFS ===\n\n")
        self.resultados_text.insert(tk.END, f"Desde: {desde}\n")
        self.resultados_text.insert(tk.END, f"Hasta: {hasta}\n\n")
        
        if existe:
            self.resultados_text.insert(tk.END, "✓ SÍ existe un camino entre los puntos\n", 'success')
            self.resultados_text.tag_config('success', foreground='green')
        else:
            self.resultados_text.insert(tk.END, "✗ NO existe un camino entre los puntos\n", 'error')
            self.resultados_text.tag_config('error', foreground='red')
    
    def mostrar_todas_rutas(self):
        desde = self.desde_entry.get().strip()
        hasta = self.hasta_entry.get().strip()
        
        if not desde or not hasta:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambos puntos")
            return
        
        rutas = self.grafo.encontrar_todas_rutas(desde, hasta)
        
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, "=== TODAS LAS RUTAS POSIBLES ===\n\n")
        self.resultados_text.insert(tk.END, f"Desde: {desde}\n")
        self.resultados_text.insert(tk.END, f"Hasta: {hasta}\n\n")
        
        if rutas:
            self.resultados_text.insert(tk.END, f"Se encontraron {len(rutas)} ruta(s):\n\n")
            
            # Ordenar rutas por longitud
            rutas_ordenadas = sorted(rutas, key=len)
            
            for i, ruta in enumerate(rutas_ordenadas, 1):
                self.resultados_text.insert(tk.END, f"Ruta {i} (longitud: {len(ruta)-1} pasos):\n")
                self.resultados_text.insert(tk.END, f"  {' -> '.join(ruta)}\n\n")
        else:
            self.resultados_text.insert(tk.END, "No se encontraron rutas entre estos puntos\n", 'error')
            self.resultados_text.tag_config('error', foreground='red')
    
    def mostrar_ruta_mas_corta(self):
        desde = self.desde_entry.get().strip()
        hasta = self.hasta_entry.get().strip()
        
        if not desde or not hasta:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambos puntos")
            return
        
        ruta = self.grafo.obtener_camino_mas_corto_bfs(desde, hasta)
        
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, "=== RUTA MÁS CORTA (BFS) ===\n\n")
        self.resultados_text.insert(tk.END, f"Desde: {desde}\n")
        self.resultados_text.insert(tk.END, f"Hasta: {hasta}\n\n")
        
        if ruta:
            self.resultados_text.insert(tk.END, f"Ruta más corta encontrada (longitud: {len(ruta)-1} pasos):\n\n")
            self.resultados_text.insert(tk.END, f"{' -> '.join(ruta)}\n", 'highlight')
            self.resultados_text.tag_config('highlight', foreground='blue', font=('Arial', 11, 'bold'))
            
            self.resultados_text.insert(tk.END, "\n\nDetalles del recorrido:\n")
            for i, punto in enumerate(ruta):
                if i < len(ruta) - 1:
                    self.resultados_text.insert(tk.END, f"  Paso {i+1}: De {punto} a {ruta[i+1]}\n")
        else:
            self.resultados_text.insert(tk.END, "No se encontró una ruta entre estos puntos\n", 'error')
            self.resultados_text.tag_config('error', foreground='red')
    
    def mostrar_matriz(self):
        """Muestra la matriz de adyacencia en una ventana nueva"""
        if self.grafo.num_puntos == 0:
            messagebox.showinfo("Información", "No hay puntos en el grafo")
            return
        
        ventana_matriz = tk.Toplevel(self.root)
        ventana_matriz.title("Matriz de Adyacencia")
        ventana_matriz.geometry("600x400")
        
        # Frame con scroll
        canvas = tk.Canvas(ventana_matriz)
        scrollbar_y = ttk.Scrollbar(ventana_matriz, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(ventana_matriz, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Crear encabezados
        ttk.Label(scrollable_frame, text="", width=15).grid(row=0, column=0)
        for j in range(self.grafo.num_puntos):
            nombre = self.grafo.indice_a_nombre[j][:10]  # Truncar nombres largos
            ttk.Label(scrollable_frame, text=nombre, width=10).grid(row=0, column=j+1)
        
        # Crear filas
        for i in range(self.grafo.num_puntos):
            nombre = self.grafo.indice_a_nombre[i][:10]
            ttk.Label(scrollable_frame, text=nombre, width=15).grid(row=i+1, column=0)
            
            for j in range(self.grafo.num_puntos):
                valor = self.grafo.matriz[i][j]
                color = "green" if valor == 1 else "black"
                label = ttk.Label(scrollable_frame, text=str(valor), foreground=color)
                label.grid(row=i+1, column=j+1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        ttk.Button(ventana_matriz, text="Cerrar", command=ventana_matriz.destroy).pack(pady=5)
    
    def limpiar_grafo(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea limpiar todo el grafo?"):
            self.grafo = GrafoRutas()
            self.actualizar_conexiones()
            self.resultados_text.delete(1.0, tk.END)
            messagebox.showinfo("Éxito", "Grafo limpiado correctamente")
    
    def cargar_ejemplo(self):
        # Cargar un ejemplo de ciudad altiplánica
        self.grafo = GrafoRutas()
        
        # Ejemplo: Red de puntos turísticos en una ciudad altiplánica
        conexiones = [
            ("Plaza_Principal", "Catedral"),
            ("Plaza_Principal", "Mercado_Artesanal"),
            ("Plaza_Principal", "Mirador_Norte"),
            ("Catedral", "Museo_Colonial"),
            ("Catedral", "Calle_Empinada_1"),
            ("Mercado_Artesanal", "Terminal_Buses"),
            ("Mercado_Artesanal", "Barrio_Artesanos"),
            ("Mirador_Norte", "Teleferico"),
            ("Mirador_Norte", "Calle_Empinada_1"),
            ("Museo_Colonial", "Plaza_Armas"),
            ("Calle_Empinada_1", "Mirador_Sur"),
            ("Calle_Empinada_1", "Barrio_Alto"),
            ("Terminal_Buses", "Hotel_Central"),
            ("Barrio_Artesanos", "Taller_Textiles"),
            ("Teleferico", "Cerro_Sagrado"),
            ("Plaza_Armas", "Palacio_Gobierno"),
            ("Mirador_Sur", "Barrio_Alto"),
            ("Barrio_Alto", "Iglesia_San_Pedro"),
            ("Hotel_Central", "Restaurant_Tipico"),
            ("Taller_Textiles", "Cooperativa_Artesanal"),
            ("Cerro_Sagrado", "Ruinas_Antiguas"),
            ("Palacio_Gobierno", "Biblioteca_Municipal"),
            ("Iglesia_San_Pedro", "Escuela_Musica"),
            ("Restaurant_Tipico", "Mercado_Artesanal"),
            ("Cooperativa_Artesanal", "Plaza_Principal"),
            ("Ruinas_Antiguas", "Sendero_Arqueologico"),
            ("Biblioteca_Municipal", "Universidad"),
            ("Escuela_Musica", "Teatro_Municipal"),
            ("Teatro_Municipal", "Plaza_Principal")
        ]
        
        for punto1, punto2 in conexiones:
            self.grafo.agregar_conexion(punto1, punto2)
        
        self.actualizar_conexiones()
        
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, "=== EJEMPLO CARGADO ===\n\n")
        self.resultados_text.insert(tk.END, "Se ha cargado un ejemplo de una ciudad altiplánica con:\n")
        self.resultados_text.insert(tk.END, f"- {len(self.grafo.obtener_puntos())} puntos turísticos\n")
        self.resultados_text.insert(tk.END, f"- {len(conexiones)} conexiones\n\n")
        self.resultados_text.insert(tk.END, "Pruebe buscando rutas entre:\n")
        self.resultados_text.insert(tk.END, "- Plaza_Principal y Ruinas_Antiguas\n")
        self.resultados_text.insert(tk.END, "- Terminal_Buses y Cerro_Sagrado\n")
        self.resultados_text.insert(tk.END, "- Mercado_Artesanal y Universidad\n")
    
    def mostrar_info(self):
        info = """
SISTEMA DE ANÁLISIS DE RUTAS - INFORMACIÓN

1. ESTRUCTURA DE DATOS - MATRIZ DE ADYACENCIA:
   - Matriz bidimensional (lista de listas)
   - matriz[i][j] = 1 si hay conexión entre i y j
   - matriz[i][j] = 0 si no hay conexión
   - Mapeo de nombres a índices con diccionarios

2. VENTAJAS DE LA MATRIZ:
   - Verificación de conexión en O(1)
   - Fácil de entender y visualizar
   - Buena para grafos densos
   - No requiere imports especiales

3. IMPLEMENTACIÓN SIN LIBRARIES:
   - Sin defaultdict: Usamos diccionarios normales
   - Sin deque: Usamos lista con pop(0) para FIFO
   - Todo con estructuras básicas de Python

4. ALGORITMOS:
   - DFS: Usa lista como pila (pop al final)
   - BFS: Usa lista como cola (pop(0) al inicio)
   - Ambos funcionan igual de eficientes

5. COMPLEJIDAD:
   - Espacio: O(V²) donde V = número de vértices
   - Agregar conexión: O(1)
   - Verificar conexión: O(1)
   - DFS/BFS: O(V²) en el peor caso

6. NOTA SOBRE EFICIENCIA:
   - pop(0) en lista es O(n), pero para grafos
     pequeños/medianos la diferencia es mínima
   - Para grafos muy grandes, deque sería mejor
"""
        
        ventana_info = tk.Toplevel(self.root)
        ventana_info.title("Información del Sistema")
        ventana_info.geometry("600x500")
        
        text_widget = scrolledtext.ScrolledText(ventana_info, wrap=tk.WORD, width=70, height=25)
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, info)
        text_widget.config(state='disabled')
        
        ttk.Button(ventana_info, text="Cerrar", command=ventana_info.destroy).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionRutas(root)
    root.mainloop()
