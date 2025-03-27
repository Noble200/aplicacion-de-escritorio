# desktop_app/app.py

import sys
import os

# Añadir el directorio padre al path para encontrar el módulo shared
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from shared.models import ProductRepository, Product

import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkScrollableFrame, CTkToplevel
from PIL import Image, ImageTk
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class StockControlApp:
    def __init__(self):
        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Control de Stock - Sistema en Tiempo Real")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Inicializar el repositorio de productos
        self.product_repo = ProductRepository()
        
        # Crear la interfaz
        self.create_ui()
        
        # Cargar productos iniciales
        self.load_products()
        
        # Configurar el listener para cambios en tiempo real
        self.watch_products()
    
    def create_ui(self):
        """Crea la interfaz de usuario con CustomTkinter"""
        
        # Frame principal con diseño de cuadrícula
        self.main_frame = CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame superior para título y botones
        self.header_frame = CTkFrame(self.main_frame)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Título
        self.title_label = CTkLabel(
            self.header_frame, 
            text="CONTROL DE INVENTARIO", 
            font=("Roboto", 24, "bold")
        )
        self.title_label.pack(side="left", padx=10)
        
        # Frame para botones de acción
        self.button_frame = CTkFrame(self.header_frame)
        self.button_frame.pack(side="right", padx=10)
        
        # Botones
        self.add_button = CTkButton(
            self.button_frame,
            text="Nuevo Producto",
            font=("Roboto", 12),
            command=self.add_product,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.add_button.pack(side="left", padx=5)
        
        self.refresh_button = CTkButton(
            self.button_frame,
            text="Actualizar",
            font=("Roboto", 12),
            command=self.load_products,
            fg_color="#17a2b8",
            hover_color="#138496"
        )
        self.refresh_button.pack(side="left", padx=5)
        
        # Frame para búsqueda
        self.search_frame = CTkFrame(self.main_frame)
        self.search_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_label = CTkLabel(
            self.search_frame,
            text="Buscar:",
            font=("Roboto", 12)
        )
        self.search_label.pack(side="left", padx=(10, 5))
        
        self.search_entry = CTkEntry(
            self.search_frame,
            font=("Roboto", 12),
            width=300,
            placeholder_text="Buscar por nombre o categoría..."
        )
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_products)
        
        # Cabecera de la tabla
        self.header_columns_frame = CTkFrame(self.main_frame)
        self.header_columns_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Cabeceras de columnas
        headers = ["ID", "Nombre", "Cantidad", "Precio", "Categoría", "Última Actualización", "Acciones"]
        widths = [80, 200, 100, 100, 150, 200, 150]
        
        for i, header in enumerate(headers):
            header_label = CTkLabel(
                self.header_columns_frame,
                text=header,
                font=("Roboto", 12, "bold"),
                width=widths[i]
            )
            header_label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Ajustar columnas
        self.header_columns_frame.grid_columnconfigure(1, weight=1)
        
        # Frame para la lista de productos (scrollable)
        self.product_list_frame = CTkScrollableFrame(
            self.main_frame,
            label_text="",
        )
        self.product_list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame de estado
        self.status_frame = CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.status_label = CTkLabel(
            self.status_frame,
            text="Conectando con Firebase...",
            font=("Roboto", 12)
        )
        self.status_label.pack(side="left", padx=10)
        
        # Variable para almacenar las referencias a las filas de productos
        self.product_rows = []
    
    def load_products(self):
        """Carga los productos desde Firebase y los muestra en la tabla"""
        # Limpiar la lista actual
        for widget in self.product_list_frame.winfo_children():
            widget.destroy()
        
        self.product_rows = []
        
        # Actualizar estado
        self.status_label.configure(text="Cargando productos...")
        
        try:
            # Obtener productos
            products = self.product_repo.get_all()
            
            # Crear filas para cada producto
            for i, product in enumerate(products):
                self.create_product_row(product, i)
            
            # Actualizar estado
            self.status_label.configure(text=f"Total: {len(products)} productos")
            
        except Exception as e:
            self.status_label.configure(text=f"Error al cargar productos: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
    
    def create_product_row(self, product, row_index):
        """Crea una fila en la tabla para mostrar un producto"""
        # Frame para la fila
        row_frame = CTkFrame(self.product_list_frame)
        row_frame.pack(fill="x", pady=2)
        row_frame.product = product  # Guardar referencia al producto
        
        # Añadir columnas con datos del producto
        # ID
        id_text = product.id[:8] + "..." if product.id and len(product.id) > 8 else product.id or ""
        id_label = CTkLabel(
            row_frame,
            text=id_text,
            font=("Roboto", 11),
            width=80
        )
        id_label.grid(row=0, column=0, padx=5, pady=8, sticky="w")
        
        # Nombre
        name_label = CTkLabel(
            row_frame,
            text=str(product.name),
            font=("Roboto", 11),
            width=200
        )
        name_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        
        # Cantidad
        quantity_label = CTkLabel(
            row_frame,
            text=str(product.quantity),
            font=("Roboto", 11),
            width=100
        )
        quantity_label.grid(row=0, column=2, padx=5, pady=8, sticky="w")
        
        # Precio
        price_label = CTkLabel(
            row_frame,
            text=f"${float(product.price):.2f}",
            font=("Roboto", 11),
            width=100
        )
        price_label.grid(row=0, column=3, padx=5, pady=8, sticky="w")
        
        # Categoría
        category_label = CTkLabel(
            row_frame,
            text=str(product.category),
            font=("Roboto", 11),
            width=150
        )
        category_label.grid(row=0, column=4, padx=5, pady=8, sticky="w")
        
        # Última actualización
        update_text = ""
        if isinstance(product.last_updated, datetime):
            update_text = product.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        else:
            update_text = str(product.last_updated)
            
        update_label = CTkLabel(
            row_frame,
            text=update_text,
            font=("Roboto", 11),
            width=200
        )
        update_label.grid(row=0, column=5, padx=5, pady=8, sticky="w")
        
        # Botones de acción
        action_frame = CTkFrame(row_frame)
        action_frame.grid(row=0, column=6, padx=5, pady=5, sticky="e")
        
        # Botón Editar
        edit_button = CTkButton(
            action_frame,
            text="Editar",
            font=("Roboto", 11),
            width=70,
            height=25,
            command=lambda p=product: self.edit_product(p),
            fg_color="#007bff",
            hover_color="#0069d9"
        )
        edit_button.pack(side="left", padx=2)
        
        # Botón Eliminar
        delete_button = CTkButton(
            action_frame,
            text="Eliminar",
            font=("Roboto", 11),
            width=70,
            height=25,
            command=lambda p=product: self.delete_product(p),
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_button.pack(side="left", padx=2)
        
        # Guardar referencia a la fila
        self.product_rows.append((row_frame, product.id))
    
    def filter_products(self, event=None):
        """Filtra los productos según el texto de búsqueda"""
        search_text = self.search_entry.get().lower()
        
        for row, product_id in self.product_rows:
            product = row.product
            if (search_text in str(product.name).lower() or 
                search_text in str(product.category).lower()):
                row.pack(fill="x", pady=2)
            else:
                row.pack_forget()
    
    def add_product(self):
        """Abre una ventana para añadir un nuevo producto"""
        self.open_product_form()
    
    def edit_product(self, product):
        """Abre una ventana para editar un producto existente"""
        self.open_product_form(product)
    
    def open_product_form(self, product=None):
        """Abre un formulario para añadir o editar un producto"""
        # Crear ventana
        form_window = CTkToplevel(self.root)
        form_window.title("Añadir Producto" if product is None else "Editar Producto")
        form_window.geometry("500x400")
        form_window.resizable(False, False)
        form_window.grab_set()  # Hacer modal
        
        # Frame principal
        main_frame = CTkFrame(form_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = CTkLabel(
            main_frame,
            text="AÑADIR PRODUCTO" if product is None else "EDITAR PRODUCTO",
            font=("Roboto", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Formulario
        form_frame = CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Campos del formulario
        # Nombre
        name_label = CTkLabel(form_frame, text="Nombre:", font=("Roboto", 12))
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        name_var = tk.StringVar(value=product.name if product else "")
        name_entry = CTkEntry(
            form_frame,
            font=("Roboto", 12),
            width=300,
            textvariable=name_var
        )
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Cantidad
        quantity_label = CTkLabel(form_frame, text="Cantidad:", font=("Roboto", 12))
        quantity_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        quantity_var = tk.StringVar(value=str(product.quantity) if product else "0")
        quantity_entry = CTkEntry(
            form_frame,
            font=("Roboto", 12),
            width=300,
            textvariable=quantity_var
        )
        quantity_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Precio
        price_label = CTkLabel(form_frame, text="Precio:", font=("Roboto", 12))
        price_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        price_var = tk.StringVar(value=f"{float(product.price):.2f}" if product else "0.00")
        price_entry = CTkEntry(
            form_frame,
            font=("Roboto", 12),
            width=300,
            textvariable=price_var
        )
        price_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Categoría
        category_label = CTkLabel(form_frame, text="Categoría:", font=("Roboto", 12))
        category_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        category_var = tk.StringVar(value=product.category if product else "")
        category_entry = CTkEntry(
            form_frame,
            font=("Roboto", 12),
            width=300,
            textvariable=category_var
        )
        category_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        
        # Botones
        button_frame = CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        cancel_button = CTkButton(
            button_frame,
            text="Cancelar",
            font=("Roboto", 12),
            width=100,
            command=form_window.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        cancel_button.pack(side="right", padx=5)
        
        def save_product():
            """Guarda o actualiza el producto en Firebase"""
            try:
                # Validar campos
                name = name_var.get().strip()
                if not name:
                    messagebox.showwarning("Validación", "El nombre del producto es obligatorio")
                    return
                
                try:
                    quantity = int(quantity_var.get().strip())
                    if quantity < 0:
                        raise ValueError("La cantidad debe ser un número positivo")
                except ValueError:
                    messagebox.showwarning("Validación", "La cantidad debe ser un número entero positivo")
                    return
                
                try:
                    # Permitir tanto punto como coma como separador decimal
                    price_str = price_var.get().strip().replace(',', '.')
                    price = float(price_str)
                    if price < 0:
                        raise ValueError("El precio debe ser un número positivo")
                except ValueError:
                    messagebox.showwarning("Validación", "El precio debe ser un número positivo")
                    return
                
                category = category_var.get().strip()
                
                if product:  # Editar producto existente
                    product.name = name
                    product.quantity = quantity
                    product.price = price
                    product.category = category
                    self.product_repo.update(product)
                    messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                else:  # Crear nuevo producto
                    new_product = Product(
                        name=name,
                        quantity=quantity,
                        price=price,
                        category=category
                    )
                    self.product_repo.add(new_product)
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")
                
                form_window.destroy()
                
                # La tabla se actualizará automáticamente gracias al listener
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar producto: {str(e)}")
        
        save_button = CTkButton(
            button_frame,
            text="Guardar",
            font=("Roboto", 12),
            width=100,
            command=save_product,
            fg_color="#28a745",
            hover_color="#218838"
        )
        save_button.pack(side="right", padx=5)
    
    def delete_product(self, product):
        """Elimina un producto tras confirmación"""
        if messagebox.askyesno("Confirmar eliminación", 
                              f"¿Estás seguro de eliminar el producto '{product.name}'?"):
            try:
                self.product_repo.delete(product.id)
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                # La tabla se actualizará automáticamente gracias al listener
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
    
    def watch_products(self):
        """Configura un listener para detectar cambios en la base de datos Firebase"""
        def on_snapshot(col_snapshot, changes, read_time):
            # Necesitamos ejecutar la actualización en el hilo principal de Tkinter
            self.root.after(0, self.load_products)
        
        # Iniciar listener
        self.listener = self.product_repo.listen_for_changes(on_snapshot)
        self.status_label.configure(text="Conectado - Escuchando cambios en tiempo real")
    
    def on_closing(self):
        """Método llamado cuando se cierra la ventana"""
        # Detener el listener
        if hasattr(self, 'listener'):
            self.listener.unsubscribe()
        
        # Cerrar la ventana
        self.root.destroy()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()