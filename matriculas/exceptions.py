class ErroMatricula(Exception):
    """Classe base para todas exceções relacionadas a matrícula"""
    pass

class ErroPagamento(ErroMatricula):
    """Exceção para erros relacionados a pagamento"""
    pass

class AssinaturaExiste(ErroMatricula):
    """Exceção para tentativa de criar assinatura quando já existe uma ativa (Pendente ou não cancelada.)"""
    pass

class AssinaturaCancelada(ErroMatricula):
    """Exceção para tentativa de cancelar assinatura já cancelada."""
    pass