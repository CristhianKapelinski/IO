
# Simulação de Gerenciamento de Entrada e Saída com Interrupções

Este projeto é uma simulação de um sistema operacional que gerencia operações de entrada e saída (E/S) utilizando interrupções. A simulação ilustra o comportamento do sistema ao lidar com dispositivos de E/S de diferentes prioridades, tratando interrupções e restaurando o contexto de um processo interrompido.

## Funcionalidades

- **Simulação de dispositivos de E/S**:
  - Teclado, Impressora, Disco, Mouse, Alto-Falante.
  - Prioridades diferentes para cada dispositivo.
- **Interrupções aleatórias**:
  - Dispositivos geram interrupções aleatórias durante a execução do processo principal.
- **Armazenamento e restauração de contexto**:
  - O estado do processo principal é salvo antes de atender uma interrupção e restaurado após o tratamento.
- **Fila de prioridade para interrupções**:
  - Dispositivos de maior prioridade têm suas interrupções tratadas primeiro.
- **Registro detalhado de eventos em log**:
  - Indicação do tempo, dispositivo, prioridade, estado do processo antes e após o tratamento.

## Pré-requisitos

Para executar este projeto, você precisa de Python 3.6 ou superior instalado em sua máquina.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/CristhianKapelinski/IO.git
   cd IO
   ```

## Execução do Programa

Para executar a simulação, use o comando:

```bash
python InputOutput.py
```

Após a execução, consulte o arquivo `simulacao_log.txt` para ver o registro detalhado dos eventos.

## Estrutura do Código

O código é dividido em três componentes principais:

### 1. Classe `Dispositivo`
Representa os dispositivos de E/S que geram interrupções. Atributos e métodos principais:
- **Atributos**:
  - `nome`: Nome do dispositivo.
  - `prioridade`: Prioridade da interrupção (menor valor = maior prioridade).
  - `tempoMinimo` e `tempoMaximo`: Intervalo de tempo de tratamento (em ciclos de clock).
- **Métodos**:
  - `gerarInterrupcao()`: Cria uma interrupção aleatória com informações do dispositivo.

### 2. Classe `GerenciadorDeInterrupcoes`
Gerencia as interrupções em uma fila de prioridade e registra os eventos em um log.
- **Atributos**:
  - `filaPrioridade`: Gerencia as interrupções em ordem de prioridade.
  - `log`: Lista de eventos registrados.
- **Métodos**:
  - `adicionarInterrupcao()`: Adiciona uma interrupção à fila.
  - `tratarInterrupcao()`: Trata a interrupção de maior prioridade e registra os eventos.

### 3. Classe `ProcessoSimulado`
Representa o processo principal em execução contínua.
- **Atributos**:
  - `id`: Identificador único do processo.
  - `contexto`: Estado atual do processo (estado, contador de operações).
- **Métodos**:
  - `executar()`: Simula a execução do processo e incrementa o contador de operações.

## Exemplo de Uso

1. Ao iniciar a simulação, o processo principal começa a ser executado.
2. Interrupções são geradas aleatoriamente e tratadas de acordo com as prioridades dos dispositivos.
3. O log (`simulacao_log.txt`) documenta os eventos, incluindo:
   - Geração de interrupções.
   - Armazenamento e restauração do contexto do processo.
   - Tempos e estados antes e após o tratamento de cada interrupção.

Exemplo de log:

```
Log da Simulação de Gerenciamento de E/S com Interrupções
==================================================

[Tempo 0] - Processo principal ID: 1 em execução. Operação #1.
[Tempo 1] - Interrupção gerada por Teclado - Prioridade: 1.
[Tempo 1] - Interrupção: Teclado - Prioridade: 1 - Armazenando contexto do processo ID: 1 - Estado Atual: {'estado': 'Executando', 'contadorOperacoes': 1}.
[Tempo 1] - Tratando a interrupção do Teclado - Tempo Estimado: 2 ciclos.
[Tempo 3] - Interrupção tratada. Restaurando contexto do processo ID: 1.
[Tempo 3] - Processo principal ID: 1 em execução. Operação #2.
```

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).