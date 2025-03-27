# shared/firebase_config.py

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json
import sys

class FirebaseConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConfig, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        """Inicializa la conexión con Firebase"""
        # Obtener la ruta al archivo de credenciales
        cred_path = self.get_credentials_path()
        
        # Si la aplicación de Firebase ya está inicializada, no la inicialices de nuevo
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Error al inicializar Firebase: {e}")
                # Crear un archivo de credenciales de ejemplo
                self.create_example_cred_file(cred_path)
                return None
        
        # Inicializar Firestore
        self.db = firestore.client()
        return self.db
    
    def get_credentials_path(self):
        """Obtiene la ruta al archivo de credenciales de Firebase"""
        # Primero, verificar si está definido como variable de entorno
        if 'FIREBASE_CONFIG' in os.environ:
            return os.environ['FIREBASE_CONFIG']
            
        # Luego, buscar en la ubicación relativa al script
        if getattr(sys, 'frozen', False):
            # Si estamos en un ejecutable
            base_path = os.path.dirname(sys.executable)
        else:
            # Si estamos en desarrollo
            base_path = os.path.dirname(os.path.dirname(__file__))
            
        return os.path.join(base_path, 'serviceAccountKey.json')
    
    def create_example_cred_file(self, path):
        """Crea un archivo de credenciales de ejemplo"""
        example_cred = {
            "type": "service_account",
            "project_id": "your-project-id",
            "private_key_id": "your-private-key-id",
            "private_key": "your-private-key",
            "client_email": "your-client-email",
            "client_id": "your-client-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "your-client-cert-url"
        }
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(example_cred, f, indent=2)
        
        print(f"⚠️ Se ha creado un archivo de credenciales de ejemplo en {path}")
        print("⚠️ Por favor, reemplázalo con tus propias credenciales de Firebase.")
    
    def get_db(self):
        """Retorna la instancia de la base de datos"""
        return self.db