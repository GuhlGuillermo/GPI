import pytest
from datetime import datetime
from src.domain.exceptions import OutOfHoursException, MinimumOrderException, InvalidPaymentException
from src.domain.models import User, Order
from src.use_cases.order_use_cases import CreateOrderUseCase

# === MOCKS DE CAPA DE INFRAESTRUCTURA ===
# No necesitamos Mongo para probar el negocio gracias a Clean Architecture.
class MockUserRepository:
    def __init__(self, mock_user=None):
        self.mock_user = mock_user
        
    def get_by_id(self, user_id):
        return self.mock_user

    def save(self, user):
        pass

class MockOrderRepository:
    def save(self, order):
        pass

# === CASOS DE PRUEBA ===

def test_order_minimum_price():
    repo = MockOrderRepository()
    user_repo = MockUserRepository()
    
    use_case = CreateOrderUseCase(repo, user_repo)
    
    # 1 Momo cuesta 6.50 -> 6.50€ No llega al mínimo de 15€.
    items = [{'dish_id': 'D1', 'name': 'Momo', 'snapshot_price': 6.50, 'quantity': 1}]
    
    with pytest.raises(MinimumOrderException) as excinfo:
        use_case.execute('U1', items, '1234123412341234')
        
    assert "importe mínimo es de 15€" in str(excinfo.value)

def test_order_bad_credit_card():
    repo = MockOrderRepository()
    user_repo = MockUserRepository()
    use_case = CreateOrderUseCase(repo, user_repo)
    
    # Llega a los 15 por cantidad
    items = [{'dish_id': 'D1', 'name': 'Momo', 'snapshot_price': 10.0, 'quantity': 2}]
    
    with pytest.raises(InvalidPaymentException):
        # Faltan dígitos o son letras
        use_case.execute('U1', items, '1234') 

def test_fidelity_discount_applied(monkeypatch):
    """Prueba que el descuento de 5 euros cada 100 aplicados"""
    # Fijamos una hora falsa a mano para saltarnos las restricciones de "fin de semana" durante el test
    class MockDatetime:
        @classmethod
        def now(cls):
            # Lunes (0) a las 14:00 (Aceptable)
            return datetime(2026, 4, 13, 14, 0, 0)
    monkeypatch.setattr('src.use_cases.order_use_cases.datetime', MockDatetime)

    # Creamos un usuario que ya gastó 250€ históricamente -> Deberían darle (2 * 5) = 10€ de dto.
    loyal_user = User(id="U_LO", role="CLIENT", historial_gasto_total=250.0)
    
    user_repo = MockUserRepository(mock_user=loyal_user)
    use_case = CreateOrderUseCase(MockOrderRepository(), user_repo)
    
    # Compra algo de 20€
    items = [{'dish_id': 'D2', 'name': 'Tikka', 'snapshot_price': 20.0, 'quantity': 1}]
    
    order = use_case.execute("U_LO", items, '1111222233334444')
    
    assert order.pricing.subtotal == 20.0
    assert order.pricing.loyalty_discount_applied == 10.0
    assert order.pricing.total == 10.0 # 20 - 10
