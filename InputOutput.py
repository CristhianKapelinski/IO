import random
from queue import PriorityQueue


class Dispositivo:
    def __init__(self, nome, prioridade, tempoMinimo, tempoMaximo):
        self.nome = nome
        self.prioridade = prioridade
        self.tempoMinimo = tempoMinimo
        self.tempoMaximo = tempoMaximo

    def gerarInterrupcao(self):
        return {
            "dispositivo": self.nome,
            "prioridade": self.prioridade,
            "tempoTratamento": random.randint(self.tempoMinimo, self.tempoMaximo)
        }


class GerenciadorDeInterrupcoes:
    def __init__(self):
        self.filaPrioridade = PriorityQueue()
        self.log = []

    def adicionarInterrupcao(self, interrupcao):
        self.filaPrioridade.put((interrupcao["prioridade"], interrupcao))

    def tratarInterrupcao(self, processo, registrarLog, tempoAtual):
        if not self.filaPrioridade.empty():
            prioridade, interrupcao = self.filaPrioridade.get()
            estadoAnterior = processo.contexto.copy()
            registrarLog(f"[Tempo {tempoAtual}] - Interrupção: {interrupcao['dispositivo']} "
                         f"- Prioridade: {prioridade} - Armazenando contexto do processo "
                         f"ID: {processo.id} - Estado Atual: {estadoAnterior}.")
            processo.contexto["estado"] = f"Tratando {interrupcao['dispositivo']}"
            registrarLog(f"[Tempo {tempoAtual}] - Tratando a interrupção do {interrupcao['dispositivo']} "
                         f"- Tempo Estimado: {interrupcao['tempoTratamento']} ciclos.")
            tempoAtual += interrupcao["tempoTratamento"]
            registrarLog(f"[Tempo {tempoAtual}] - Interrupção tratada. "
                         f"Restaurando contexto do processo ID: {processo.id}.")
            processo.contexto["estado"] = "Executando"
            return interrupcao, tempoAtual
        return None, tempoAtual


class ProcessoSimulado:
    contadorId = 0

    def __init__(self):
        ProcessoSimulado.contadorId += 1
        self.id = ProcessoSimulado.contadorId
        self.contexto = {"estado": "Executando", "contadorOperacoes": 0}

    def executar(self, registrarLog, tempoAtual):
        self.contexto["estado"] = "Executando"
        self.contexto["contadorOperacoes"] += 1
        registrarLog(f"[Tempo {tempoAtual}] - Processo principal ID: {self.id} "
                     f"em execução. Operação #{self.contexto['contadorOperacoes']}.")
        tempoAtual += 1 
        return tempoAtual


def registrarLogArquivo(mensagem, nomeArquivo="simulacao_log.txt"):
    with open(nomeArquivo, "a") as arquivo:
        arquivo.write(mensagem + "\n")


def main():
    dispositivos = [
        Dispositivo("Teclado", 1, 2, 3),        # Alta prioridade, 2-3 ciclos
        Dispositivo("Impressora", 2, 3, 5),    # Média prioridade, 3-5 ciclos
        Dispositivo("Disco", 3, 4, 6),         # Baixa prioridade, 4-6 ciclos
        Dispositivo("Mouse", 4, 1, 2),         # Prioridade menor, 1-2 ciclos
        Dispositivo("Alto-Falante", 5, 1, 1)   # Prioridade mínima, 1 ciclo fixo
    ]

    gerenciador = GerenciadorDeInterrupcoes()
    processo = ProcessoSimulado()
    tempoAtual = 0
    tempoTotalInterrupcoes = 0
    with open("simulacao_log.txt", "w") as arquivo:
        arquivo.write("Log da Simulação de Gerenciamento de E/S com Interrupções\n")
        arquivo.write("=" * 50 + "\n\n")

    for operation in range(20):
        print(f"\n[Operação {operation + 1}]")

        tempoAtual = processo.executar(lambda msg: registrarLogArquivo(msg), tempoAtual)

        if random.randint(0, 10) < 2:
            dispositivoEscolhido = random.choice(dispositivos)
            interrupcao = dispositivoEscolhido.gerarInterrupcao()
            gerenciador.adicionarInterrupcao(interrupcao)
            print(f"Interrupção gerada por {interrupcao['dispositivo']} com prioridade {interrupcao['prioridade']}")
            registrarLogArquivo(f"[Tempo {tempoAtual}] - Interrupção gerada por {interrupcao['dispositivo']} "
                                f"- Prioridade: {interrupcao['prioridade']}.")
        while not gerenciador.filaPrioridade.empty():
            interrupcaoTratada, tempoAtual = gerenciador.tratarInterrupcao(processo, lambda msg: registrarLogArquivo(msg), tempoAtual)
            if interrupcaoTratada:
                tempoTotalInterrupcoes += interrupcaoTratada["tempoTratamento"]

    registrarLogArquivo(f"\nTempo total gasto em interrupções: {tempoTotalInterrupcoes} ciclos.")
    print("\nA simulação foi concluída. Consulte o arquivo 'simulacao_log.txt' para ver o log completo.")

if __name__ == "__main__":
    main()
