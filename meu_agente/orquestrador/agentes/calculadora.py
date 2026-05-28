import math

def python_calculator(expression: str) -> str:
    """Executa uma expressão matemática em Python de forma segura e retorna o resultado."""
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names.update({"abs": abs, "round": round})
    try:
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return f"Resultado exato: {result}"
    except Exception as e:
        return f"Erro ao calcular a expressão: {str(e)}"
