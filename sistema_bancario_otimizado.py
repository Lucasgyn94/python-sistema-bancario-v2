import textwrap

def menu():
    menu = """
    =============== Menu ===============
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNovo usuário
    [5]\tNova Conta
    [6]\tListar Contas
    [7]\tTransferir
    [8]\tConsultar Saldo
    [9]\tEncerramento de Conta
    [0]\tSair
    """
    return input(textwrap.dedent(menu))

def depositar(conta, valor):
    if valor > 0:
        conta['saldo'] += valor
        conta['extrato'] += f"Depósito:\t R$ {valor:.2f}\n"
        print("=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@Operação falhou! Valor informado é inválido. @@@")

def sacar(conta, valor, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > conta['saldo']
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Falha! Você não possui saldo suficiente.")
    elif excedeu_limite:
        print("Falha! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Falha! Você excedeu o limite de saques.")
    elif valor > 0:
        conta['saldo'] -= valor
        conta['extrato'] += f"Saque:\t R$ {valor:.2f}\n"
        numero_saques += 1
        print("=== Saque realizado com sucesso! ===")
    else:
        print("Operação falhou! Valor informado é inválido.")

    return numero_saques

def exibir_extrato(conta):
    print("=============== EXTRATO ===============")
    print("Não foram realizadas movimentações." if not conta['extrato'] else conta['extrato'])
    print(f"\nSaldo:\tR$ {conta['saldo']:.2f}")
    print("======================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com este cpf!")
        return
    
    nome = input("Informe o nome do usuário: ")
    data_nascimento = input("Informe a sua data de nascimento:  ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })
    print("===Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def filtrar_conta(numero_conta, contas):
    contas_filtradas = [conta for conta in contas if str(conta["numero_conta"]) == str(numero_conta)]
    return contas_filtradas[0] if contas_filtradas else None

def transferir(contas):
    numero_conta_origem = input("Informe o número da conta de origem: ")
    conta_origem = filtrar_conta(numero_conta_origem, contas)

    if not conta_origem:
        print("\n@@@Conta de origem não encontrada! @@@")
        return
    
    numero_conta_destino = input("Informe o número da conta de destino: ")
    conta_destino = filtrar_conta(numero_conta_destino, contas)

    if not conta_destino:
        print("\n@@@Conta de destino não encontrada! @@@")
        return
    
    valor = float(input("Informe o valor a ser transferido: "))

    if valor <= 0:
        print("\n@@@Operação falhou! Valor informado é inválido. @@@")
        return
    
    if conta_origem['saldo'] < valor:
        print("\n@@@Operação falhou! Você não possui saldo suficiente. @@@")
        return
    
    conta_origem['saldo'] -= valor
    conta_destino['saldo'] += valor

    conta_origem['extrato'] += f"Transferência enviada:\tR$ {valor:.2f}\n"
    conta_destino['extrato'] += f"Transferência recebida:\tR$ {valor:.2f}\n"

    print(f"Transferência:\tR$ {valor:.2f}")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o cpf do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {
            "agencia": agencia,
            "numero_conta": str(numero_conta),
            "usuario": usuario,
            "saldo": 0,
            "extrato": ""
        }
    
    print("\n@@@Usuário não encontrado! @@@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))
    
def consultar_saldo(contas):
    numero_conta = str(input("Informe o número da conta: "))
    conta = filtrar_conta(numero_conta, contas)

    if conta:
        print(f"Saldo atual: R$ {conta['saldo']:.2f}")
    else:
        print("Conta não encontrada.")

def fechar_conta(contas):
    numero_conta = input("Informe o número da conta a ser fechada: ")
    conta = filtrar_conta(numero_conta, contas)

    if conta:
        if conta['saldo'] != 0:
            print("Conta não pode ser fechada, pois ainda possui saldo.")
        else:
            contas.remove(conta)
            print("Conta fechada com sucesso!")
    else:
        print("Conta não encontrada.")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    limite = 500
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True: 
        opcao = menu()
        
        if opcao == "1":
            numero_conta = input("Informe o número da conta para depósito: ")
            conta = filtrar_conta(numero_conta, contas)
            if conta:
                valor = float(input("Informe o valor a ser depositado: "))
                depositar(conta, valor)
            else:
                print("Conta não encontrada.")

        elif opcao == "2":
            numero_conta = input("Informe o número da conta para saque: ")
            conta = filtrar_conta(numero_conta, contas)
            if conta:
                valor = float(input("Informe o valor a ser sacado: "))
                numero_saques = sacar(
                    conta,
                    valor=valor,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES
                )
            else:
                print("Conta não encontrada.")
           
        elif opcao == "3":
            numero_conta = input("Informe o número da conta para exibir o extrato: ")
            conta = filtrar_conta(numero_conta, contas)
            if conta:
                exibir_extrato(conta)
            else:
                print("Conta não encontrada.")

        elif opcao == "4":
            criar_usuario(usuarios)
        
        elif opcao == "5":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                numero_conta += 1
        
        elif opcao == "6":
            listar_contas(contas)
        
        elif opcao == "7":
            transferir(contas)
        
        elif opcao == "8":
            consultar_saldo(contas)
        
        elif opcao == "9":
            fechar_conta(contas)

        elif opcao == "0":
            break
        
        else:
            print("Opção inválida! Selecione uma entre as opções!")

main()
