from datetime import datetime
from src.domain.models import DailyBilling
from src.infrastructure.database.mongo_repos import MongoBillingRepository

class BillingBufferManager:
    """
    Singleton que almacena la facturación del día en memoria RAM para no saturar 
    las operaciones a base de datos.
    Se limpia periódicamente haciendo un 'flush' a MongoDB.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            instance = super(BillingBufferManager, cls).__new__(cls)
            instance._init_state()
            cls._instance = instance
        return cls._instance

    def _init_state(self):
        self.repo = MongoBillingRepository()
        self.fecha_actual = datetime.now().strftime('%Y-%m-%d')
        self.total_facturado = 0.0
        self.cantidad_pedidos = 0
        self.pedidos_refs = []
        self.pedidos_en_ram = []
        self.usuarios_en_ram = {}
        self.MAX_BUFFER_SIZE = 500  # Límite anti-saturación

    def add_order(self, order, user=None):
        hoy = datetime.now().strftime('%Y-%m-%d')
        
        # Si cambiamos de día, volcamos el día anterior
        if hoy != self.fecha_actual:
            self.flush_to_db()
            self.fecha_actual = hoy
            
        self.total_facturado += order.importe_total
        self.cantidad_pedidos += 1
        self.pedidos_refs.append(order.id_pedido)
        self.pedidos_en_ram.append(order)
        if user:
            self.usuarios_en_ram[user.id_usuario] = user
        
        # Volcado de seguridad para no consumir toda la RAM del VPS
        if self.cantidad_pedidos >= self.MAX_BUFFER_SIZE:
            self.flush_to_db()

    def flush_to_db(self):
        """Vuelca la RAM actual a Mongo y limpia el buffer"""
        if self.cantidad_pedidos == 0:
            return # Nada que guardar
            
        # Dependencias de inyección tardía
        from src.infrastructure.database.mongo_repos import MongoOrderRepository, MongoUserRepository
        order_repo = MongoOrderRepository()
        user_repo = MongoUserRepository()
        
        # 1. Volcar los pedidos de RAM a MongoDB
        for order_ram in self.pedidos_en_ram:
            order_repo.save(order_ram)
            
        # 2. Volcar los usuarios de RAM a MongoDB
        for user_ram in self.usuarios_en_ram.values():
            user_repo.save(user_ram)
            
        billing = DailyBilling(
            fecha=self.fecha_actual,
            total_facturado=self.total_facturado,
            cantidad_pedidos=self.cantidad_pedidos,
            pedidos_refs=self.pedidos_refs
        )
        self.repo.add_billing_data(billing)
        
        # Resetear estado de la RAM
        self.total_facturado = 0.0
        self.cantidad_pedidos = 0
        self.pedidos_refs = []
        self.pedidos_en_ram = []
        self.usuarios_en_ram = {}

    def get_orders_in_ram(self) -> list:
        return self.pedidos_en_ram

    def get_current_snapshot(self) -> dict:
        """Devuelve una foto rápida del estado consolidado + lo que hay en RAM"""
        # Obtenemos la fecha más reciente guardada en base de datos para mostrarla en el dashboard,
        # en caso de discrepancias de zona horaria entre Docker (UTC) y Host (Local)
        latest_db_data = self.repo.collection.find_one({}, sort=[('fecha', -1)])
        
        fecha_a_mostrar = self.fecha_actual
        db_total = 0.0
        db_cantidad = 0

        if latest_db_data:
            # Si en DB hay datos más recientes o iguales, los usamos
            fecha_a_mostrar = max(self.fecha_actual, latest_db_data['fecha'])
            if fecha_a_mostrar == latest_db_data['fecha']:
                db_total = latest_db_data.get('total_facturado', 0.0)
                db_cantidad = latest_db_data.get('cantidad_pedidos', 0)
        
        # Si la fecha de la RAM coincide con la que vamos a mostrar, sumamos la RAM
        ram_total = self.total_facturado if self.fecha_actual == fecha_a_mostrar else 0.0
        ram_cantidad = self.cantidad_pedidos if self.fecha_actual == fecha_a_mostrar else 0
        
        return {
            "fecha": fecha_a_mostrar,
            "total_estimado": db_total + ram_total,
            "cantidad_pedidos": db_cantidad + ram_cantidad,
            "notas": "Incluye datos consolidados más recientes y la memoria en vivo aplicable."
        }
