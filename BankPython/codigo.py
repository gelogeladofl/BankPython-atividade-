from datetime import datetime, timezone, timedelta

# Configurações Globais Parametrizadas
TAXA_OPERACIONAL_SAQUE = 2.50
LIMITE_DIARIO_SAQUE = 1000.00
LIMITE_MENSAL_SAQUE = 5000.00
LIMITE_MAX_CHEQUE_ESPECIAL_NOVA_CONTA = 5000.00  # Teto máximo para novas contas
LIMITE_MAX_SALDO_INICIAL = 10000.00             # Limite máximo de depósito inicial

ADM_USER = "lucas"
ADM_PASSWORD = "123"

# Definindo o fuso horário de Brasília (UTC-3) fixo
FUSO_BRASILIA = timezone(timedelta(hours=-3))

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
▓ [4] Informações do Banco                                           ▓
▓                                                                    ▓
▓ [0] Sair                                                           ▓
▓                                                                    ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
""")

# --- NOVA TELA DE INFORMAÇÕES DO BANCO ---
def exibir_informacoes_banco():
    """Exibe as taxas e limites vigentes no banco, emoldurado com o caractere ▓"""
    print("\n" + "▓" * 70)
    print(f"▓{'INFORMAÇÕES E TARIFAS VIGENTES':^68}▓")
    print("▓                                                                    ▓")
    print("▓" + "▓" * 68 + "▓")
    print(f"▓{' ':68}▓")
    print(f"▓ {f'- Tarifa de Saque por Operação: R$ {TAXA_OPERACIONAL_SAQUE:.2f}':<66} ▓")
    print(f"▓ {f'- Limite de Saque Diário: R$ {LIMITE_DIARIO_SAQUE:.2f}':<66} ▓")
    print(f"▓ {f'- Limite de Saque Mensal: R$ {LIMITE_MENSAL_SAQUE:.2f}':<66} ▓")
    print(f"▓ {f'- Cheque Especial Máximo Inicial: R$ {LIMITE_MAX_CHEQUE_ESPECIAL_NOVA_CONTA:.2f}':<66} ▓")
    print(f"▓ {f'- Saldo Inicial Máximo Permitido: R$ {LIMITE_MAX_SALDO_INICIAL:.2f}':<66} ▓")
    print(f"▓{' ':68}▓")
    print("▓" * 70)
    input("\nPressione [ENTER] para voltar ao menu principal...")

# --- FUNÇÕES DE VALIDAÇÃO ---
def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

def obter_data_valida(mensagem):
    while True:
        data_str = input(mensagem).strip()
        try:
            data_digitada = datetime.strptime(data_str, "%d/%m/%Y").date()
            hoje_brasilia = datetime.now(FUSO_BRASILIA).date()
            
            if data_digitada > hoje_brasilia:
                print(f"Erro: A data não pode ser posterior ao dia de hoje ({hoje_brasilia.strftime('%d/%m/%Y')}).")
                continue
                
            return data_str
        except ValueError:
            print("Erro: Data inválida ou formato incorreto. Use DD/MM/AAAA.")

def obter_valor_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Erro: Digite um valor numérico válido.")

# --- SISTEMA CENTRAL ---
def registrar_transacao(cpf, tipo, valor):
    data_hora = datetime.now(FUSO_BRASILIA).strftime("%d/%m/%Y %H:%M:%S")
    transacao = {
        "tipo": tipo,
        "valor": valor,
        "saldo_resultante": contas_bancarias[cpf]["saldo"],
        "data_hora": data_hora
    }
    contas_bancarias[cpf]["extrato"].append(transacao)

# --- FLUXO DE CRIAÇÃO ---
def abrir_conta():
    print("\n--- Abrindo conta ---")
    
    while True:
        cpf = input("Digite o CPF (apenas números): ").strip()
        if not validar_cpf(cpf):
            print("Erro: CPF inválido. Tente novamente.")
            continue
        if cpf in contas_bancarias:
            print("Erro: Já existe uma conta vinculada a este CPF.")
            return
        break
        
    data_nasc = obter_data_valida("Digite a data de nascimento (DD/MM/AAAA): ")
    
    # Validação do Saldo Inicial Limitado a R$ 10.000,00
    while True:
        saldo_inicial = obter_valor_float("Digite o saldo inicial: R$ ")
        if 0 <= saldo_inicial <= LIMITE_MAX_SALDO_INICIAL:
            break
        print(f"Erro: O saldo inicial deve ser entre R$ 0.00 e R$ {LIMITE_MAX_SALDO_INICIAL:.2f}.")

    while True:
        print(f"Nota: O limite máximo pré-aprovado para novas contas é de R$ {LIMITE_MAX_CHEQUE_ESPECIAL_NOVA_CONTA:.2f}")
        limite_cheque = obter_valor_float("Digite o limite do cheque especial pré-aprovado: R$ ")
        if 0 <= limite_cheque <= LIMITE_MAX_CHEQUE_ESPECIAL_NOVA_CONTA:
            break
        print(f"Erro: O limite deve ser entre R$ 0.00 e R$ {LIMITE_MAX_CHEQUE_ESPECIAL_NOVA_CONTA:.2f}.")

    contas_bancarias[cpf] = {
        "data_nasc": data_nasc,
        "saldo": saldo_inicial,
        "limite_cheque": limite_cheque,
        "extrato": []
    }
    registrar_transacao(cpf, "Abertura de Conta", saldo_inicial)
    print("Conta criada com sucesso!")

# --- SEÇÃO DO CLIENTE LOGADO ---
def acessar_conta():
    print("\n--- Login no BankPython ---")
    cpf = input("Digite o seu CPF: ").strip()
    
    if cpf not in contas_bancarias:
        print("Erro: Conta não encontrada.")
        return

    while True:
        print(f"\n| ÁREA DO CLIENTE | CPF: {cpf}")
        print(f"Saldo Atual: R$ {contas_bancarias[cpf]['saldo']:.2f}")
        print(f"Cheque Especial Disponível: R$ {contas_bancarias[cpf]['limite_cheque']:.2f}")
        print("-" * 40)
        print("[1] Depositar")
        print("[2] Sacar")
        print("[3] Consultar Extrato")
        print("[4] Encerrar Conta")
        print("[0] Logout (Sair da Conta)")

        opcao = input("Escolha a operação: ").strip()

        if opcao == "1":
            valor_deposito = obter_valor_float("Digite o valor do depósito: R$ ")
            if valor_deposito > 0:
                contas_bancarias[cpf]["saldo"] += valor_deposito
                registrar_transacao(cpf, "Depósito", valor_deposito)
                print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!")
            else:
                print("Erro: O valor do depósito deve ser maior que zero.")

        elif opcao == "2":
            global TAXA_OPERACIONAL_SAQUE, LIMITE_DIARIO_SAQUE, LIMITE_MENSAL_SAQUE
            valor_saque = obter_valor_float("Digite o valor do saque: R$ ")

            if valor_saque <= 0:
                print("Erro: Valor inválido.")
                continue

            conta = contas_bancarias[cpf]

            agora = datetime.now(FUSO_BRASILIA)
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

            if (valor_saque + TAXA_OPERACIONAL_SAQUE) <= (conta["saldo"] + conta["limite_cheque"]):
                conta["saldo"] -= (valor_saque + TAXA_OPERACIONAL_SAQUE)
                registrar_transacao(cpf, "Saque", valor_saque)
                if TAXA_OPERACIONAL_SAQUE > 0:
                    registrar_transacao(cpf, "Tarifa de Saque", TAXA_OPERACIONAL_SAQUE)
                print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")
            else:
                print("Erro: Saldo e limite de cheque especial insuficientes.")

        elif opcao == "3":
            ultimas_transacoes = contas_bancarias[cpf]["extrato"][-5:]
            print(f"\n EXTRATO DE CONTA (Últimas {len(ultimas_transacoes)} movimentações):")
            if not ultimas_transacoes:
                print("Nenhuma movimentação encontrada.")
            for t in ultimas_transacoes:
                print(f"[{t['data_hora']}] {t['tipo']}: R$ {t['valor']:.2f} (Saldo: R$ {t['saldo_resultante']:.2f})")

        elif opcao == "4":
            if contas_bancarias[cpf]["saldo"] == 0:
                confirmacao = input("Tem certeza que deseja encerrar sua conta? (S/N): ").strip().upper()
                if confirmacao == 'S':
                    del contas_bancarias[cpf]
                    print("Sua conta foi encerrada com sucesso!")
                    break 
                else:
                    print("Operação cancelada.")
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
    usuario = input("Usuário ADM: ").strip()
    senha = input("Senha ADM: ").strip()

    if usuario != ADM_USER or senha != ADM_PASSWORD:
        print("Erro: Credenciais administrativas incorretas!")
        return

    global TAXA_OPERACIONAL_SAQUE, LIMITE_DIARIO_SAQUE, LIMITE_MENSAL_SAQUE, LIMITE_MAX_CHEQUE_ESPECIAL_NOVA_CONTA
    while True:
        print("\n| PAINEL ADMINISTRATIVO BANKPYTHON |")
        print("[1] Listar todas as contas ativas")
        print("[2] Configurar Taxas e Limites Globais")
        print("[3] Alterar Cheque Especial de uma Conta Específica")
        print("[4] Ver patrimônio total do banco")
        print("[0] Voltar ao menu principal")

        opcao_adm = input("Escolha a ação administrativa: ").strip()

        if opcao_adm == "1":
            print("\n--- Contas Cadastradas ---")
            if not contas_bancarias:
                print("Nenhuma conta ativa no momento.")
            for cpf, dados in contas_bancarias.items():
                print(f"CPF: {cpf[:3]}.***.***-{cpf[-2:]} | Saldo: R$ {dados['saldo']:.2f} | Cheque Especial: R$ {dados['limite_cheque']:.2f}")

        elif opcao_adm == "2":
            while True:
                print("\n--- CONFIGURAÇÕES DE TAXAS E LIMITES ---")
                print(f"[1] Alterar Tarifa de Saque (Atual: R$ {TAXA_OPERACIONAL_SAQUE:.2f})")
                print(f"[2] Alterar Limite Diário   (Atual: R$ {LIMITE_DIARIO_SAQUE:.2f})")
                print(f"[3] Alterar Limite Mensal   (Atual: R$ {LIMITE_MENSAL_SAQUE:.2f})")
                print(f"[4] Alterar Teto Máximo p/ Novas Contas (Atual: R$ {LIMITE_MAX_CHEQUE_ESPECIAL_NOVA_CONTA:.2f})")
                print("[0] Voltar")

                sub_opcao = input("Escolha o parâmetro: ").strip()
                if sub_opcao == "1":
                    TAXA_OPERACIONAL_SAQUE = max(0.0, obter_valor_float("Nova tarifa: R$ "))
                elif sub_opcao == "2":
                    LIMITE_DIARIO_SAQUE = max(0.0, obter_valor_float("Novo limite diário: R$ "))
                elif sub_opcao == "3":
                    LIMITE_MENSAL_SAQUE = max(0.0, obter_valor_float("Novo limite mensal: R$ "))
                elif sub_opcao == "4":
                    LIMITE_MAX_CHEQUE_ESPECIAL_NOVA_CONTA = max(0.0, obter_valor_float("Novo teto de cheque especial para novas contas: R$ "))
                elif sub_opcao == "0":
                    break

        elif opcao_adm == "3":
            print("\n--- Alterar Limite de Conta Específica ---")
            cpf_alvo = input("Digite o CPF da conta que deseja alterar (apenas números): ").strip()
            
            if cpf_alvo in contas_bancarias:
                print(f"Conta encontrada! Limite de Cheque Especial Atual: R$ {contas_bancarias[cpf_alvo]['limite_cheque']:.2f}")
                novo_limite = obter_valor_float("Digite o novo valor do Cheque Especial: R$ ")
                
                if novo_limite >= 0:
                    contas_bancarias[cpf_alvo]['limite_cheque'] = novo_limite
                    print(f"Sucesso! O novo limite de cheque especial para o CPF {cpf_alvo} é R$ {novo_limite:.2f}")
                    registrar_transacao(cpf_alvo, f"Alteração de Limite ADM (Novo: R$ {novo_limite:.2f})", 0.0)
                else:
                    print("Erro: O limite não pode ser negativo.")
            else:
                print("Erro: Conta não encontrada.")

        elif opcao_adm == "4":
            total_banco = sum(conta["saldo"] for conta in contas_bancarias.values())
            print(f"\nPatrimônio Total Custodiado: R$ {total_banco:.2f}")

        elif opcao_adm == "0":
            break
        else:
            print("Opção inválida.")

# --- LOOP PRINCIPAL ---
def main():
    while True:
        exibir_menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1": abrir_conta()
        elif opcao == "2": acessar_conta() 
        elif opcao == "3": painel_adm()
        elif opcao == "4": exibir_informacoes_banco() # Nova chamada adicionada aqui!
        elif opcao == "0":
            print("Saindo do BankPython... Até logo!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
