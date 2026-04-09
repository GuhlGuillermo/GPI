import uuid
from datetime import datetime
from src.domain.models import Order, OrderPricing
from src.domain.exceptions import OutOfHoursException, MinimumOrderException, InvalidPaymentException

class CreateOrderUseCase:
    """
    Reglas de Negocio a aplicar:
    1. Horario: Solo entre 13:00 y 16:00, no en fines de semana (Sábado=5, Domingo=6).
    2. Importe mínimo: 15€.
    3. Validación de Tarjeta: Solo 16 dígitos exactos numéricos.
    4. Fidelización: Descuento de 5€ por cada 100€ de historial.
    """
    def __init__(self, order_repo, user_repo):
        # La inyección de dependencias nos aísla de Mongo
        self.order_repo = order_repo
        self.user_repo = user_repo

    def execute(self, user_id: str, items_data: list, credit_card: str) -> Order:
        # 1. Validación de Horario (Se asume la hora actual del servidor/restaurante)
        now = datetime.now()
        is_weekend = now.weekday() >= 5
        if is_weekend or not (13 <= now.hour < 16):
            raise OutOfHoursException("Solo se aceptan pedidos de lunes a viernes entre las 13:00 y las 16:00.")

        # 2. Validación Fake Tarjeta
        if not credit_card.isdigit() or len(credit_card) != 16:
            raise InvalidPaymentException("La tarjeta debe contener exactamente 16 dígitos numéricos.")

        # 3. Construcción y cálculo del subtotal (En un caso real los items se verificarían contra el CatalogoRepo)
        subtotal = sum([item['snapshot_price'] * item['quantity'] for item in items_data])
        
        # 4. Importe mínimo
        if subtotal < 15.00:
            raise MinimumOrderException(f"El importe mínimo es de 15€. El carrito actual es de {subtotal}€.")

        # 5. Fidelización de clientes registrados
        discount = 0.0
        user = self.user_repo.get_by_id(user_id) if user_id else None
        if user and user.role == "CLIENT":
            # Calcular tramos de 100€ -> 5€ cada uno
            discount = (user.historial_gasto_total // 100) * 5.0
            
            # (Limitamos que el descuento no haga el pedido gratis por lógica comercial)
            discount = min(discount, subtotal - 0.01)

        # Montaje final de la Entidad
        pricing = OrderPricing(subtotal=subtotal, loyalty_discount_applied=discount)
        
        order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            items=items_data, # Aquí los convertiríamos a dataclass OrderItem
            pricing=pricing,
            status="RECEIVED"
        )

        # Usar la infraestructura inyectada para guardar
        self.order_repo.save(order)
        
        # (Opcional) Guardar gastos del usuario para el futuro si así corresponde
        if user:
            user.historial_gasto_total += order.pricing.total
            self.user_repo.save(user)

        return order
