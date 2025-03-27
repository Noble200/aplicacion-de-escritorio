# shared/models.py

from datetime import datetime
from firebase_admin import firestore
from .firebase_config import FirebaseConfig

class Product:
    """Clase para representar un producto en el inventario"""
    
    def __init__(self, id=None, name="", quantity=0, price=0.0, category="", last_updated=None):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category
        self.last_updated = last_updated or datetime.now()
    
    @staticmethod
    def from_dict(source, id=None):
        """Crea un objeto Product desde un diccionario"""
        # Versión simplificada para evitar problemas de tipos
        last_updated = source.get("last_updated")
        
        # Usar fecha actual si no hay fecha o no se puede convertir
        if last_updated is None:
            last_updated = datetime.now()
        
        return Product(
            id=id,
            name=source.get("name", ""),
            quantity=source.get("quantity", 0),
            price=source.get("price", 0.0),
            category=source.get("category", ""),
            last_updated=last_updated
        )
    
    def to_dict(self):
        """Convierte el objeto Product a un diccionario para Firestore"""
        return {
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "category": self.category,
            "last_updated": firestore.SERVER_TIMESTAMP
        }
    
    def __str__(self):
        return f"{self.name} (ID: {self.id}) - Cantidad: {self.quantity}, Precio: ${self.price:.2f}"


class ProductRepository:
    """Clase para gestionar operaciones CRUD de productos en Firestore"""
    
    def __init__(self):
        self.db = FirebaseConfig().get_db()
        self.collection = self.db.collection("products")
    
    def get_all(self):
        """Obtiene todos los productos"""
        products = []
        for doc in self.collection.stream():
            product = Product.from_dict(doc.to_dict(), id=doc.id)
            products.append(product)
        return products
    
    def get_by_id(self, product_id):
        """Obtiene un producto por su ID"""
        doc = self.collection.document(product_id).get()
        if doc.exists:
            return Product.from_dict(doc.to_dict(), id=doc.id)
        return None
    
    def add(self, product):
        """Añade un nuevo producto"""
        doc_ref = self.collection.document()
        doc_ref.set(product.to_dict())
        product.id = doc_ref.id
        return product
    
    def update(self, product):
        """Actualiza un producto existente"""
        if not product.id:
            raise ValueError("El producto debe tener un ID para actualizarlo")
        
        self.collection.document(product.id).update(product.to_dict())
        return product
    
    def delete(self, product_id):
        """Elimina un producto por su ID"""
        self.collection.document(product_id).delete()
        return True
    
    def listen_for_changes(self, callback):
        """
        Escucha cambios en la colección de productos y llama a la función callback
        cuando ocurra un cambio.
        """
        return self.collection.on_snapshot(callback)