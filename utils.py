def validar_entero(input):
    try:
        entero = int(input)
        return True
    except ValueError:
        return False
