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
        self.contadorUnico = 0

    def adicionarInterrupcao(self, interrupcao, registrarLog, tempoAtual):
        self.contadorUnico += 1
        self.filaPrioridade.put((-interrupcao["prioridade"], self.contadorUnico, interrupcao))
        self.registrarFila(registrarLog, tempoAtual)

    def registrarFila(self, registrarLog, tempoAtual):
        if not self.filaPrioridade.empty():
            estadoFila = []
            for item in list(self.filaPrioridade.queue):
                estadoFila.append(f"{item[2]['dispositivo']} (Prioridade: {-item[0]})")
            registrarLog(f"[Tempo {tempoAtual}] - Estado da fila de prioridades: {', '.join(estadoFila)}.")

    def tratarInterrupcao(self, processo, registrarLog, tempoAtual):
        if not self.filaPrioridade.empty():
            _, _, interrupcao = self.filaPrioridade.get()
            estadoAnterior = processo.contexto.copy()
            registrarLog(f"[Tempo {tempoAtual}] - Interrupção: {interrupcao['dispositivo']} "
                         f"- Prioridade: {-_} - Armazenando contexto do processo "
                         f"ID: {processo.id} - Estado Atual: {estadoAnterior}.")
            processo.contexto["estado"] = f"Tratando {interrupcao['dispositivo']}"
            registrarLog(f"[Tempo {tempoAtual}] - Tratando a interrupção do {interrupcao['dispositivo']} "
                         f"- Tempo Estimado: {interrupcao['tempoTratamento']} ciclos.")
            tempoAtual += interrupcao["tempoTratamento"]
            registrarLog(f"[Tempo {tempoAtual}] - Interrupção tratada. "
                         f"Restaurando contexto do processo ID: {processo.id}.")
            processo.contexto["estado"] = "Executando"
            self.registrarFila(registrarLog, tempoAtual)
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
    random.seed(42)
    dispositivos = [
        Dispositivo("Teclado", 5, 2, 3), 
        Dispositivo("Impressora", 3, 3, 5),
        Dispositivo("Disco", 1, 4, 6), 
        Dispositivo("Mouse", 4, 1, 2),
        Dispositivo("Alto-Falante", 2, 1, 1) 
    ]

    gerenciador = GerenciadorDeInterrupcoes()
    processo = ProcessoSimulado()
    tempoAtual = 0
    tempoTotalInterrupcoes = 0
    with open("simulacao_log.txt", "w") as arquivo:
        arquivo.write("Log da Simulação de Gerenciamento de E/S com Interrupções\n")
        arquivo.write("=" * 50 + "\n\n")

    for _ in range(5):
        tempoAtual = processo.executar(lambda msg: registrarLogArquivo(msg), tempoAtual)

        if random.randint(0, 10) < 3:
            dispositivosEscolhidos = random.sample(dispositivos, k=min(len(dispositivos), random.randint(1, 3)))
            for dispositivoEscolhido in dispositivosEscolhidos:
                interrupcao = dispositivoEscolhido.gerarInterrupcao()
                gerenciador.adicionarInterrupcao(interrupcao, lambda msg: registrarLogArquivo(msg), tempoAtual)
                registrarLogArquivo(f"[Tempo {tempoAtual}] - Interrupção gerada por {interrupcao['dispositivo']} "
                                     f"- Prioridade: {interrupcao['prioridade']}.")

        while not gerenciador.filaPrioridade.empty():
            interrupcaoTratada, tempoAtual = gerenciador.tratarInterrupcao(processo, lambda msg: registrarLogArquivo(msg), tempoAtual)
            if interrupcaoTratada:
                tempoTotalInterrupcoes += interrupcaoTratada["tempoTratamento"]

    registrarLogArquivo(f"\nTempo total gasto em interrupções: {tempoTotalInterrupcoes} ciclos.")
    print("A simulação foi concluída. Consulte o arquivo 'simulacao_log.txt' para ver o log completo.")

if __name__ == "__main__":
    main()
