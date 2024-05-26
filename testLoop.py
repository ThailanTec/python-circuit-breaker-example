import requests
from pybreaker import CircuitBreaker, CircuitBreakerError
from colorama import Fore, Style

# Configurações do circuit breaker
failure_threshold = 3  # Número máximo de falhas consecutivas permitidas
success_threshold = 5  # Número mínimo de sucessos consecutivos necessários
# Tempo de espera em segundos antes de tentar novamente após o circuit breaker bloquear a chamada
reset_timeout = 3

# Cria o circuit breaker
breaker = CircuitBreaker(fail_max=failure_threshold,
                         reset_timeout=reset_timeout)


@breaker
def call_endpoint(value):
    # Se for par, chame o endpoint /failure
    # Se for ímpar, chame o endpoint /random
    endpoint = '/failure' if value % 2 == 0 else '/random'

    response = requests.get(f'http://localhost:5000{endpoint}')
    # Lança uma exceção caso a resposta não seja bem-sucedida
    response.raise_for_status()
    return response.json()


# Executa o loop para testar o circuit breaker
for i in range(1, 11):
    print(f"Executando iteração {i}")

    try:
        result = call_endpoint(i)
        print(Fore.GREEN + 'Chamada bem-sucedida!')
        print(Fore.GREEN + f"Resultado: {result}")
        print(Style.RESET_ALL)
    except CircuitBreakerError:
        print(Fore.RED + 'Chamada bloqueada pelo circuit breaker')
        print(Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f'Erro ao chamar o endpoint: {e}')
        print(Style.RESET_ALL)

    print("---------------------------")

print("Loop concluído!")