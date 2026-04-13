import uuid
from datetime import datetime
from src.domain.models import Order, OrderItem
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
        self.order_repo = order_repo
        self.user_repo = user_repo

    def execute(self, user_id: str, items_data: list, credit_card: str, dir_entrega: str = "", nombre: str = "", email: str = "") -> Order:
        now = datetime.now()
        is_weekend = now.weekday() >= 5
        if is_weekend or not (13 <= now.hour < 16):
            raise OutOfHoursException("Solo se aceptan pedidos de lunes a viernes entre las 13:00 y las 16:00.")

        if not credit_card.isdigit() or len(credit_card) != 16:
            raise InvalidPaymentException("La tarjeta debe contener exactamente 16 dígitos numéricos.")

        subtotal = sum([item['precio_plato'] * item['cantidad'] for item in items_data])
        
        if subtotal < 15.00:
            raise MinimumOrderException(f"El importe mínimo es de 15€. El carrito actual es de {subtotal}€.")

        discount = 0.0
        
        # Lógica de autocompletado de Usuario por email o creación silenciosa
        user = None
        if email:
            user = self.user_repo.get_by_email(email)
            if not user:
                from src.domain.models import User
                user = User(
                    id_usuario=str(uuid.uuid4()),
                    nombre=nombre,
                    email=email,
                    rol="CLIENT"
                )
                self.user_repo.save(user) # Persistimos el nuevo invitado
                
        # Si fue proporcionado un ID (por ejemplo token autenticado más adelante) pero la lógica por email no operó
        if not user and user_id and user_id != "invitado":
            user = self.user_repo.get_by_id(user_id)

        if user and user.rol == "CLIENT":
            discount = (user.gasto_total // 100) * 5.0
            discount = min(discount, subtotal - 0.01)
            user.es_cliente_habitual = user.gasto_total > 50.0

        importe_final = max(0.0, subtotal - discount)
        
        order_items = [
            OrderItem(
                id_plato=item['id_plato'],
                nombre_plato=item['nombre_plato'],
                precio_plato=item['precio_plato'],
                cantidad=item['cantidad']
            ) for item in items_data
        ]

        # Asegurar que el id_usuario en el ticket sea el real (si creamos la cuenta en el aire)
        final_user_id = user.id_usuario if user else user_id

        order = Order(
            id_pedido=str(uuid.uuid4()),
            id_usuario=final_user_id,
            items=order_items,
            importe_total=importe_final,
            estado="RECIBIDO",
            dir_entrega=dir_entrega,
            hora_entrega=datetime.now(),
            info_pago="TARJETA"
        )

        self.order_repo.save(order)
        
        if user:
            user.gasto_total += order.importe_total
            self.user_repo.save(user)

        return order
