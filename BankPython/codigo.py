import datetime

# Configurações Globais Parametrizadas
TAXA_OPERACIONAL_SAQUE = 2.50
LIMITE_DIARIO_SAQUE = 1000.00
LIMITE_MENSAL_SAQUE = 5000.00

ADM_USER = "lucas"
ADM_PASSWORD = "123"

contas_bancarias = {}

def exibir_menu_principal():
    print("""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                        SEJA BEM-VINDO AO                           ▓   
▓                           BANKPYTHON                               ▓
▓                                                                    ▓  
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                    ▓
▓ [1] Abrir Conta                                                    ▓
▓ [2] Acessar Conta (Entrar na sua área logada)                      ▓
▓ [3] Painel ADM                                                     ▓
▓                                                                    ▓
▓ [0] Sair                                                           ▓
▓                                                                    ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
""")

def registrar_transacao(cpf, tipo, valor):
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    transacao = {
        "tipo": tipo,
        "valor": valor,
        "saldo_resultante": contas_bancarias[cpf]["saldo"],
        "data_hora": data_hora
    }
    contas_bancarias[cpf]["extrato"].append(transacao)

def obter_valor_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Erro: Digite um valor numérico válido.")

# --- FLUXO DE CRIAÇÃO ---
def abrir_conta():
    print("\n--- Abrindo conta ---")
    cpf = input("Digite o CPF (apenas números): ")
    if cpf in contas_bancarias:
        print("Erro: Já existe uma conta vinculada a este CPF.")
        return
    data_nasc = input("Digite a data de nascimento (DD/MM/AAAA): ")
    saldo_inicial = obter_valor_float("Digite o saldo inicial: R$ ")
    limite_cheque = obter_valor_float("Digite o limite do cheque especial: R$ ")

    contas_bancarias[cpf] = {
        "data_nasc": data_nasc,
        "saldo": saldo_inicial,
        "limite_cheque": limite_cheque,
        "extrato": []
    }
    registrar_transacao(cpf, "Abertura de Conta", saldo_inicial)
    print("Conta criada com sucesso!")

# --- SEÇÃO DO CLIENTE LOGADO (Sua sugestão de melhoria) ---
def acessar_conta():
    print("\n--- Login no BankPython ---")
    cpf = input("Digite o seu CPF: ")
    if cpf not in contas_bancarias:
        print("Erro: Conta não encontrada.")
        return

    # O cliente digitou o CPF certo? Entra na área logada dele
    while True:
        print(f"\n ÁREA DO CLIENTE | CPF: {cpf}")
        print(f"Saldo Atual: R$ {contas_bancarias[cpf]['saldo']:.2f}")
        print("-" * 40)
        print("[1] Depositar")
        print("[2] Sacar")
        print("[3] Consultar Extrato")
        print("[4] Encerrar Conta")
        print("[0] Logout (Sair da Conta)")
        
        opcao = input("Escolha a operação: ")

        if opcao == "1":
            valor_deposito = obter_valor_float("Digite o valor do depósito: R$ ")
            if valor_deposito > 0:
                contas_bancarias[cpf]["saldo"] += valor_deposito
                registrar_transacao(cpf, "Depósito", valor_deposito)
                print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!")
                
        elif opcao == "2":
            global TAXA_OPERACIONAL_SAQUE, LIMITE_DIARIO_SAQUE, LIMITE_MENSAL_SAQUE
            valor_saque = obter_valor_float("Digite o valor do saque: R$ ")
            
            if valor_saque <= 0:
                print("Erro: Valor inválido.")
                continue
                
            conta = contas_bancarias[cpf]
            
            # Validação de limites temporais
            agora = datetime.datetime.now()
            hoje_str = agora.strftime("%d/%m/%Y")
            mes_ano_str = agora.strftime("%m/%Y")
            
            total_sacado_hoje = 0.0
            total_sacado_mes = 0.0
            
            for t in conta["extrato"]:
                if t["tipo"] == "Saque":
                    data_transacao = t["data_hora"].split(" ")[0]
                    mes_ano_transacao = data_transacao[3:]
                    
                    if data_transacao == hoje_str:
                        total_sacado_hoje += t["valor"]
                    if mes_ano_transacao == mes_ano_str:
                        total_sacado_mes += t["valor"]
                        
            if total_sacado_hoje + valor_saque > LIMITE_DIARIO_SAQUE:
                print(f"\n❌ Negado! Limite diário de R$ {LIMITE_DIARIO_SAQUE:.2f} excedido.")
                continue

            if total_sacado_mes + valor_saque > LIMITE_MENSAL_SAQUE:
                print(f"\n❌ Negado! Limite mensal de R$ {LIMITE_MENSAL_SAQUE:.2f} excedido.")
                continue

            # Validação financeira
            if (valor_saque + TAXA_OPERACIONAL_SAQUE) <= (conta["saldo"] + conta["limite_cheque"]):
                conta["saldo"] -= (valor_saque + TAXA_OPERACIONAL_SAQUE)
                registrar_transacao(cpf, "Saque", valor_saque)
                registrar_transacao(cpf, "Tarifa de Saque", TAXA_OPERACIONAL_SAQUE)
                print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")
            else:
                print("Erro: Saldo e limite insuficientes.")

        elif opcao == "3":
            # Extrato usa o CPF da sessão atual automaticamente
            ultimas_transacoes = contas_bancarias[cpf]["extrato"][-3:] 
            print(f"\n EXTRATO DE CONTA (Últimas {len(ultimas_transacoes)} movimentações):")
            for t in ultimas_transacoes:
                print(f"[{t['data_hora']}] {t['tipo']}: R$ {t['valor']:.2f} (Saldo: R$ {t['saldo_resultante']:.2f})")

        elif opcao == "4":
            # Regra de encerramento
            if contas_bancarias[cpf]["saldo"] == 0:
                del contas_bancarias[cpf]
                print("Sua conta foi encerrada com sucesso. Obrigado por usar o BankPython!")
                break # Sai da área logada já que a conta sumiu
            else:
                print(f"Erro: Não é possível encerrar. Zere seu saldo antes (Saldo atual: R$ {contas_bancarias[cpf]['saldo']:.2f})")

        elif opcao == "0":
            print("Efetuando logout... Voltando ao menu inicial.")
            break
        else:
            print("Opção inválida.")

# --- PAINEL ADMINISTRATIVO ---
def painel_adm():
    print("\n--- Autenticação ADM ---")
    usuario = input("Usuário ADM: ")
    senha = input("Senha ADM: ")

    if usuario != ADM_USER or senha != ADM_PASSWORD:
        print("Erro: Credenciais administrativas incorretas!")
        return

    global TAXA_OPERACIONAL_SAQUE, LIMITE_DIARIO_SAQUE, LIMITE_MENSAL_SAQUE
    while True:
        print("\n  PAINEL ADMINISTRATIVO BANKPYTHON ")
        print("[1] Listar todas as contas ativas")
        print("[2] Configurar Taxas e Limites Globais")
        print("[3] Ver patrimônio total do banco")
        print("[0] Voltar ao menu principal")
        
        opcao_adm = input("Escolha a ação administrativa: ")

        if opcao_adm == "1":
            print("\n--- Contas Cadastradas ---")
            if not contas_bancarias:
                print("Nenhuma conta ativa no momento.")
            for cpf, dados in contas_bancarias.items():
                print(f"CPF: {cpf} | Saldo: R$ {dados['saldo']:.2f} | Limite Cheque: R$ {dados['limite_cheque']:.2f}")
        
        elif opcao_adm == "2":
            while True:
                print("\n---  CONFIGURAÇÕES DE TAXAS E LIMITES ---")
                print(f"[1] Alterar Tarifa de Saque (Atual: R$ {TAXA_OPERACIONAL_SAQUE:.2f})")
                print(f"[2] Alterar Limite Diário   (Atual: R$ {LIMITE_DIARIO_SAQUE:.2f})")
                print(f"[3] Alterar Limite Mensal   (Atual: R$ {LIMITE_MENSAL_SAQUE:.2f})")
                print("[0] Voltar")
                
                sub_opcao = input("Escolha o parâmetro: ")
                if sub_opcao == "1":
                    TAXA_OPERACIONAL_SAQUE = max(0.0, obter_valor_float("Nova tarifa: R$ "))
                elif sub_opcao == "2":
                    LIMITE_DIARIO_SAQUE = max(0.0, obter_valor_float("Novo limite diário: R$ "))
                elif sub_opcao == "3":
                    LIMITE_MENSAL_SAQUE = max(0.0, obter_valor_float("Novo limite mensal: R$ "))
                elif sub_opcao == "0":
                    break

        elif opcao_adm == "3":
            total_banco = sum(conta["saldo"] for conta in contas_bancarias.values())
            print(f"\nPatrimônio Total Custodiado: R$ {total_banco:.2f}")

        elif opcao_adm == "0":
            break

# --- LOOP PRINCIPAL ---
def main():
    while True:
        exibir_menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == "1": abrir_conta()
        elif opcao == "2": acessar_conta() # Abre a nova central do cliente logado
        elif opcao == "3": painel_adm()  
        elif opcao == "0":
            print("Saindo do BankPython... Até logo!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
