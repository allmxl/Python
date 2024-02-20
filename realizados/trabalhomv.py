import os
import pickle

class Processo:
    def __init__(self, pid):
        self.pid = pid

    def execute(self):
        pass

class ComputingProcess(Processo):
    def __init__(self, pid, operand1, operand2, operation):
        super().__init__(pid)
        self.operand1 = operand1
        self.operand2 = operand2
        self.operation = operation

    def execute(self):
        if self.operation == '+':
            result = self.operand1 + self.operand2
        elif self.operation == '-':
            result = self.operand1 - self.operand2
        elif self.operation == '*':
            result = self.operand1 * self.operand2
        elif self.operation == '/':
            result = self.operand1 / self.operand2
        else:
            result = None
        print(f"Resultado do cálculo (pid={self.pid}): {result}")

class WritingProcess(Processo):
    def execute(self):
        with open('computation.txt', 'a') as file:
            file.write(f"Expressão gravada pelo processo {self.pid}\n")

class ReadingProcess(Processo):
    def execute(self):
        with open('computation.txt', 'r') as file:
            expressions = file.readlines()
            for expression in expressions:
                print(f"Processo de leitura - Expressão lida: {expression.strip()}")

        # Limpar o arquivo após a leitura
        open('computation.txt', 'w').close()

class PrintingProcess(Processo):
    def execute(self):
        print(f"Imprimindo pool de processos (pid={self.pid}): Tipo - PrintingProcess")

# Implementação do sistema
class Sistema:
    def __init__(self):
        self.processos = []

    def criar_processo(self):
        tipo_processo = input("Digite o tipo de processo (Calculo, Gravacao, Leitura, Impressao): ").lower()

        if tipo_processo == 'calculo':
            operand1 = float(input("Digite o primeiro operando: "))
            operand2 = float(input("Digite o segundo operando: "))
            operation = input("Digite a operação (+, -, *, /): ")
            novo_processo = ComputingProcess(len(self.processos), operand1, operand2, operation)

        elif tipo_processo == 'gravacao':
            novo_processo = WritingProcess(len(self.processos))

        elif tipo_processo == 'leitura':
            novo_processo = ReadingProcess(len(self.processos))

        elif tipo_processo == 'impressao':
            novo_processo = PrintingProcess(len(self.processos))

        else:
            print("Tipo de processo inválido.")
            return

        self.processos.append(novo_processo)
        print(f"Processo criado com pid={len(self.processos) - 1}")

    def executar_proximo(self):
        if self.processos:
            processo_atual = self.processos.pop(0)
            processo_atual.execute()
        else:
            print("Nenhum processo para executar.")

    def executar_processo_especifico(self):
        pid = int(input("Digite o pid do processo a ser executado: "))
        if 0 <= pid < len(self.processos):
            processo_especifico = self.processos.pop(pid)
            processo_especifico.execute()
        else:
            print("Pid inválido.")

    def salvar_fila_em_arquivo(self):
        with open('fila_de_processos.pkl', 'wb') as file:
            pickle.dump(self.processos, file)
        print("Fila de processos salva em arquivo.")

    def carregar_fila_do_arquivo(self):
        if os.path.exists('fila_de_processos.pkl'):
            with open('fila_de_processos.pkl', 'rb') as file:
                self.processos = pickle.load(file)
            print("Fila de processos carregada do arquivo.")
        else:
            print("Arquivo de fila de processos não encontrado.")

# Testando o sistema
sistema = Sistema()

while True:
    print("\nOpções do sistema:")
    print("1. Criar processo")
    print("2. Executar próximo")
    print("3. Executar processo específico")
    print("4. Salvar fila de processos em arquivo")
    print("5. Carregar fila de processos do arquivo")
    print("6. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        sistema.criar_processo()
    elif opcao == '2':
        sistema.executar_proximo()
    elif opcao == '3':
        sistema.executar_processo_especifico()
    elif opcao == '4':
        sistema.salvar_fila_em_arquivo()
    elif opcao == '5':
        sistema.carregar_fila_do_arquivo()
    elif opcao == '6':
        break
    else:
        print("Opção inválida. Tente novamente.")
