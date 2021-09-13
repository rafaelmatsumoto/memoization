import redis


# O algoritmo utiliza o Redis como cache,
# e nessa classe criamos um decorator do python para salvar os valores das funções executadas em memória.
# Dessa forma, não é preciso calcular valores novamente, apenas consultar o cache
class Memoize:
    def __init__(self, f):
        self.f = f
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def __call__(self, *args):
        # Consulta o cache para verificar se o valor já foi previamente calculado
        if not self.redis.exists(*args):
            # Adiciona o valor para consultas futuras
            self.redis.set(*args, self.f(*args))
        return int(self.redis.get(*args).decode("utf-8"))


@Memoize
def factorial(x):
    """
    Função que calcula o fatorial de um número
    """
    # Condição de saída, ou de cauda
    if x == 0 or x == 1:
        return x
    else:
        return x * factorial(x - 1)


@Memoize
def superfactorial(x):
    """
    Função que calcula o superfatorial de um número
    """
    if x == 0 or x == 1:
        return factorial(x)
    else:
        return factorial(x) * superfactorial(x - 1)


for n in list(range(23)):
    superfactorial(n)

print("Finished processing")
