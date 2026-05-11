import pytest
from src.domain.models import DailyBilling
from src.use_cases.billing_buffer import BillingBufferManager

class MockBillingRepository:
    def __init__(self):
        self.storage = {}

    def add_billing_data(self, billing: DailyBilling):
        if billing.fecha not in self.storage:
            self.storage[billing.fecha] = billing
        else:
            exist = self.storage[billing.fecha]
            exist.total_facturado += billing.total_facturado
            exist.cantidad_pedidos += billing.cantidad_pedidos
            exist.pedidos_refs.extend(billing.pedidos_refs)

    def get_by_date(self, fecha: str):
        return self.storage.get(fecha)

@pytest.fixture(autouse=True)
def reset_singleton(monkeypatch):
    """
    Inyecta un MockRepository y resetea el Singleton en cada test.
    """
    BillingBufferManager._instance = None
    monkeypatch.setattr('src.use_cases.billing_buffer.MongoBillingRepository', lambda: MockBillingRepository())
    
    manager = BillingBufferManager()
    yield manager
    BillingBufferManager._instance = None

def test_buffer_memory_accumulation(reset_singleton):
    manager = reset_singleton
    
    manager.add_order("ORD-1", 15.0)
    manager.add_order("ORD-2", 20.0)
    
    # Comprobar que en memoria hay 35€ y 2 pedidos
    assert manager.total_facturado == 35.0
    assert manager.cantidad_pedidos == 2
    assert "ORD-1" in manager.pedidos_refs
    
    # Comprobar que en base de datos NO hay nada todavía (la RAM retiene)
    db_data = manager.repo.get_by_date(manager.fecha_actual)
    assert db_data is None

def test_buffer_flush(reset_singleton):
    manager = reset_singleton
    
    manager.add_order("ORD-1", 50.0)
    manager.flush_to_db()
    
    # La RAM se vacía
    assert manager.total_facturado == 0.0
    assert manager.cantidad_pedidos == 0
    
    # La DB recibe los datos
    db_data = manager.repo.get_by_date(manager.fecha_actual)
    assert db_data is not None
    assert db_data.total_facturado == 50.0
    assert db_data.cantidad_pedidos == 1

def test_buffer_auto_flush_on_max_size(reset_singleton):
    manager = reset_singleton
    manager.MAX_BUFFER_SIZE = 3 # Bajamos el límite artificialmente para el test
    
    manager.add_order("O-1", 10.0)
    manager.add_order("O-2", 10.0)
    
    # Aún no se ha llegado a 3
    assert manager.total_facturado == 20.0
    assert manager.repo.get_by_date(manager.fecha_actual) is None
    
    # Al meter el 3º, debe volcar automáticamente
    manager.add_order("O-3", 10.0)
    
    # La RAM vuelve a cero
    assert manager.total_facturado == 0.0
    
    # La DB tiene 30
    db_data = manager.repo.get_by_date(manager.fecha_actual)
    assert db_data.total_facturado == 30.0
    assert db_data.cantidad_pedidos == 3
