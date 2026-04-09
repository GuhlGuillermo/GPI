class BusinessRuleException(Exception):
    """Excepción base para violaciones de reglas de negocio."""
    pass

class OutOfHoursException(BusinessRuleException):
    pass

class MinimumOrderException(BusinessRuleException):
    pass

class InvalidPaymentException(BusinessRuleException):
    pass
