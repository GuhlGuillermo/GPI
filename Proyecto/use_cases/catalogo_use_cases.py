from domain.repository_interfaces import CatalogoRepository

class ConsultarCatalogoUseCase:
    def __init__(self, catalogo_repo: CatalogoRepository):
        self.catalogo_repo = catalogo_repo
        
    def execute(self):
        # En el futuro se puede aplicar lógica extra: filtros, paginación, etc.
        return self.catalogo_repo.listar_platos_en_carta()
