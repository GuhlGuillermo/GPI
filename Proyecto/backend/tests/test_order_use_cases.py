import pytest
from datetime import datetime
from src.domain.exceptions import OutOfHoursException, MinimumOrderException, InvalidPaymentException
from src.domain.models import User, Order
from src.use_cases.order_use_cases import CreateOrderUseCase

# === MOCKS DE CAPA DE INFRAESTRUCTURA ===
class MockUserRepository:
    def __init__(self, mock_user=None):
        self.mock_user = mock_user
        
    def get_by_id(self, user_id):
        return self.mock_user
        
    def get_by_email(self, email):
        if self.mock_user and self.mock_user.email == email:
            return self.mock_user
        return None

    def save(self, user):
        pass

class MockOrderRepository:
    def save(self, order):
        pass

# Mock para el buffer
class MockBillingBufferManager:
    def add_order(self, order_id, importe):
        pass

# === CASOS DE PRUEBA ===

@pytest.fixture(autouse=True)
def mock_billing_buffer(monkeypatch):
    """Evita que los tests unitarios afecten al singleton en RAM real o levanten dependencias de MongoDB"""
    monkeypatch.setattr('src.use_cases.billing_buffer.BillingBufferManager', lambda: MockBillingBufferManager())

def test_order_minimum_price(monkeypatch):
    class MockDatetime:
        @classmethod
        def now(cls):
            return datetime(2026, 4, 13, 14, 0, 0)
    monkeypatch.setattr('src.use_cases.order_use_cases.datetime', MockDatetime)
    
    repo = MockOrderRepository()
    user_repo = MockUserRepository()
    
    use_case = CreateOrderUseCase(repo, user_repo)
    
    # 1 Momo cuesta 6.50 -> 6.50€ No llega al mínimo de 15€.
    items = [{'id_plato': 'D1', 'nombre_plato': 'Momo', 'precio_plato': 6.50, 'cantidad': 1}]
    
    with pytest.raises(MinimumOrderException) as excinfo:
        use_case.execute('U1', items, '1234123412341234')
        
    assert "importe mínimo es de 15€" in str(excinfo.value)

def test_order_bad_credit_card(monkeypatch):
    class MockDatetime:
        @classmethod
        def now(cls):
            return datetime(2026, 4, 13, 14, 0, 0)
    monkeypatch.setattr('src.use_cases.order_use_cases.datetime', MockDatetime)

    repo = MockOrderRepository()
    user_repo = MockUserRepository()
    use_case = CreateOrderUseCase(repo, user_repo)
    
    # Llega a los 15 por cantidad
    items = [{'id_plato': 'D1', 'nombre_plato': 'Momo', 'precio_plato': 10.0, 'cantidad': 2}]
    
    with pytest.raises(InvalidPaymentException):
        # Faltan dígitos o son letras
        use_case.execute('U1', items, '1234') 

def test_fidelity_discount_applied(monkeypatch):
    """Prueba que el descuento de 5 euros cada 100 aplicados"""
    class MockDatetime:
        @classmethod
        def now(cls):
            # Lunes (0) a las 14:00 (Aceptable)
            return datetime(2026, 4, 13, 14, 0, 0)
    monkeypatch.setattr('src.use_cases.order_use_cases.datetime', MockDatetime)

    # Creamos un usuario que ya gastó 250€ históricamente -> Deberían darle (2 * 5) = 10€ de dto.
    loyal_user = User(id_usuario="U_LO", rol="CLIENT", gasto_total=250.0)
    
    user_repo = MockUserRepository(mock_user=loyal_user)
    use_case = CreateOrderUseCase(MockOrderRepository(), user_repo)
    
    # Compra algo de 20€
    items = [{'id_plato': 'D2', 'nombre_plato': 'Tikka', 'precio_plato': 20.0, 'cantidad': 1}]
    
    # user_id explícito
    order = use_case.execute("U_LO", items, '1111222233334444')
    
    # Subtotal 20.0. Descuento 10.0. Importe final = 10.0.
    assert order.importe_total == 10.0
