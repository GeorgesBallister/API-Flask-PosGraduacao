# Dentro deste modulo, est'ao presentes apenas funções que normalizam os dados


# * Normalizar CPF
def normaliza_cpf(cpf: str) -> str:
    return ''.join(ch for ch in cpf if ch.isdigit())