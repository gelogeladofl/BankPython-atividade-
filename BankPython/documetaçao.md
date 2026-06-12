# 1. Introdução

## 1.1 Objetivo do Sistema

O sistema **BankPython** tem como objetivo prover um mecanismo de gerenciamento financeiro em memória para contas correntes digitais, permitindo operações bancárias básicas com validação automática de regras de saldo, aplicação de tarifas operacionais e controle de cheque especial através de uma interface CLI.

---

## 1.2 Escopo

O sistema contempla:

* Cadastro de contas bancárias;
* Controle de saldo;
* Depósitos e saques;
* Controle de cheque especial;
* Emissão de extrato simplificado;
* Encerramento de contas.

O sistema será executado integralmente em memória RAM, sem persistência em banco de dados nesta versão MVP.

---

# 2. Visão Geral do Sistema

O sistema é composto por três módulos principais:

```text
                ┌──────────────────────┐
                │   Interface CLI      │
                └──────────┬───────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Gestão Conta   │ │ Fluxo Financeiro│ │ Histórico      │
│ CPF Único      │ │ Saque/Depósito │ │ Extrato        │
└────────────────┘ └────────────────┘ └────────────────┘
```

---
# 3. Histórias de Usuário (User Stories)

As histórias de usuário representam as necessidades identificadas durante a etapa de levantamento de requisitos junto ao cliente e servem como base para os requisitos funcionais do sistema.

## US-01 — Abertura de Conta Corrente

**Como** cliente bancário, **eu quero** abrir uma conta corrente digital **para** realizar operações financeiras de forma segura e organizada.

### Critérios de Aceitação

* Informar CPF, data de nascimento, saldo inicial e limite de cheque especial.
* O CPF não pode existir previamente no sistema.
* A conta deve ser criada com sucesso.

---

## US-02 — Realizar Depósito

**Como** cliente bancário, **eu quero** depositar dinheiro em minha conta **para** aumentar meu saldo disponível.

### Critérios de Aceitação

* O valor informado deve ser maior que zero.
* O saldo deve ser atualizado imediatamente.
* O depósito deve ser registrado no histórico de movimentações.
* Caso exista utilização do cheque especial, o depósito deve amortizar automaticamente o saldo negativo.

---

## US-03 — Realizar Saque

**Como** cliente bancário, **eu quero** sacar dinheiro da minha conta **para** utilizar meus recursos financeiros quando necessário.

### Critérios de Aceitação

* O sistema deve validar saldo e limite do cheque especial.
* Deve ser aplicada automaticamente a taxa operacional de R$ 2,50.
* O valor solicitado não pode ultrapassar o limite permitido.
* O saldo deve ser atualizado imediatamente.
* A operação deve ser registrada no histórico.

---

## US-04 — Consultar Extrato

**Como** cliente bancário, **eu quero** consultar meu extrato simplificado **para** acompanhar minhas movimentações financeiras recentes.

### Critérios de Aceitação

* O sistema deve exibir as últimas três movimentações realizadas.
* Cada movimentação deve apresentar:

  * Tipo da operação;
  * Valor movimentado;
  * Saldo resultante;
  * Data e hora da operação.

---

## US-05 — Encerrar Conta

**Como** cliente bancário, **eu quero** encerrar minha conta corrente **para** finalizar meu relacionamento com o banco digital.

### Critérios de Aceitação

* O saldo da conta deve ser igual a R$ 0,00.
* Não pode existir utilização ativa do cheque especial.
* O sistema deve confirmar o encerramento da conta.

# 4. Requisitos do Sistema

## 4.1 Requisitos Funcionais (Functional Requirements)

---

### SYS-RF-01 — Abertura de Conta Corrente

**Prioridade:** Alta

#### Descrição

O sistema deve permitir a criação de contas bancárias vinculadas a um cliente.

#### Dados obrigatórios

* CPF
* Data de nascimento
* Saldo inicial
* Limite do cheque especial

#### Critério de Aceitação

* O CPF não pode existir previamente no sistema.
* A conta deve ser criada com sucesso na estrutura de dados.

---

### SYS-RF-02 — Processamento de Depósito

**Prioridade:** Alta

#### Descrição

O sistema deve processar depósitos financeiros em contas ativas.

#### Critério de Aceitação

* O saldo deve ser atualizado imediatamente.
* Caso exista saldo negativo, o valor deve amortizar automaticamente o cheque especial.

---

### SYS-RF-03 — Processamento de Saque

**Prioridade:** Alta

#### Descrição

O sistema deve permitir saques considerando saldo disponível e cheque especial.

#### Critério de Aceitação

* O saque deve incluir taxa operacional fixa.
* O sistema deve bloquear saques acima do limite permitido.
* O saldo deve ser atualizado imediatamente.

---

### SYS-RF-04 — Emissão de Extrato Simplificado

**Prioridade:** Média

#### Descrição

O sistema deve exibir as últimas movimentações realizadas na conta.

#### Critério de Aceitação

* O extrato deve apresentar somente as últimas 3 transações.
* O sistema deve exibir:

  * tipo da operação;
  * valor;
  * saldo resultante;
  * data/hora.

---

### SYS-RF-05 — Encerramento de Conta

**Prioridade:** Média

#### Descrição

O sistema deve permitir o encerramento lógico da conta bancária.

#### Critério de Aceitação

* O saldo da conta deve ser igual a R$ 0,00.
* Não pode existir utilização ativa do cheque especial.

---

# 4.2 Regras de Negócio (Business Rules)

---

### SYS-RN-01 — Invariante de Saldo para Saques

Toda operação de saque deve obedecer à seguinte restrição matemática:

Valor_{Saque}+Taxa_{Operacional}\le Saldo_{Atual}+Limite_{ChequeEspecial}

---

### SYS-RN-02 — Tarifa Operacional Fixa

Todo saque autorizado deve debitar automaticamente uma taxa operacional fixa de R$ 2,50.

---

### SYS-RN-03 — Unicidade de CPF

O sistema deve impedir múltiplas contas vinculadas ao mesmo CPF.

---

### SYS-RN-04 — Regra de Encerramento

Contas com saldo diferente de zero não podem ser encerradas.

---

### SYS-RN-05 — Regra de Amortização Automática

Todo depósito realizado em conta com saldo negativo deve ser utilizado prioritariamente para redução do valor utilizado do cheque especial.

---

# 4.3 Requisitos Não Funcionais (Non-Functional Requirements)

---

### SYS-RNF-01 — Parametrização

A taxa operacional de saque deve estar isolada em variável configurável, permitindo futuras alterações sem modificação da lógica principal.

---

### SYS-RNF-02 — Robustez

O sistema deve tratar erros de entrada utilizando estruturas `try-except`, evitando falhas da aplicação.

---

### SYS-RNF-03 — Persistência Temporária

O sistema deve manter os dados apenas em memória RAM durante a execução da aplicação.

---

### SYS-RNF-04 — Interface CLI

O sistema deve operar exclusivamente via terminal de comandos.

---

# 5. Restrições do Sistema

* O sistema não utilizará banco de dados nesta versão.
* O sistema não possuirá autenticação de usuários.
* O sistema funcionará apenas em ambiente local.
* O sistema utilizará interface textual CLI.

---

# 6. Matriz de Rastreabilidade

| ID Requisito | Regra Associada       | Sprint   | Objetivo de Verificação          |
| ------------ | --------------------- | -------- | -------------------------------- |
| SYS-RF-01    | SYS-RN-03             | Sprint 1 | Validar CPF duplicado            |
| SYS-RF-02    | SYS-RN-05             | Sprint 1 | Validar amortização automática   |
| SYS-RF-03    | SYS-RN-01 / SYS-RN-02 | Sprint 2 | Validar saque e taxa             |
| SYS-RF-04    | N/A                   | Sprint 2 | Validar limite de 3 operações    |
| SYS-RF-05    | SYS-RN-04             | Sprint 2 | Validar bloqueio de encerramento |

---

# 7. Critérios Gerais de Aceitação

* Todas as operações devem atualizar o saldo corretamente.
* Nenhuma operação deve gerar inconsistência financeira.
* O sistema não deve encerrar inesperadamente por erro de entrada.
* O histórico deve registrar corretamente todas as operações.

  # 8. Protótipo de Interface CLI

O protótipo representa o fluxo de navegação do usuário dentro do sistema BankPython antes da implementação final em Python.

## Menu Principal

```text
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                        SEJA BEM-VINDO AO                           ▓
▓                           BANKPYTHON                               ▓
▓                                                                    ▓
▓ [1] Abrir Conta                                                    ▓
▓ [2] Acessar Conta                                                  ▓
▓ [3] Painel ADM                                                     ▓
▓                                                                    ▓
▓ [0] Sair                                                           ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
```

---

## Fluxo de Abertura de Conta

```text
Abrir Conta
     │
     ▼
Informar CPF
     │
     ▼
CPF já existe?
 ┌── Sim ──► Exibir erro
 │
 Não
 │
 ▼
Informar Data de Nascimento
     │
     ▼
Informar Saldo Inicial
     │
     ▼
Informar Limite do Cheque Especial
     │
     ▼
Criar Conta
     │
     ▼
Conta criada com sucesso
```

---

## Área do Cliente

```text
ÁREA DO CLIENTE

[1] Depositar
[2] Sacar
[3] Consultar Extrato
[4] Encerrar Conta
[0] Logout
```

---

## Fluxo de Depósito

```text
Depositar
    │
    ▼
Informar Valor
    │
    ▼
Valor válido?
 ┌── Não ──► Exibir erro
 │
 Sim
 │
 ▼
Atualizar Saldo
    │
    ▼
Registrar Transação
    │
    ▼
Operação Concluída
```

---

## Fluxo de Saque

```text
Sacar
    │
    ▼
Informar Valor
    │
    ▼
Validar Limite Diário
    │
    ▼
Validar Limite Mensal
    │
    ▼
Validar Saldo + Cheque Especial
    │
    ▼
Aplicar Taxa de R$ 2,50
    │
    ▼
Atualizar Saldo
    │
    ▼
Registrar Transação
    │
    ▼
Operação Concluída
```

---

## Fluxo de Consulta de Extrato

```text
Consultar Extrato
        │
        ▼
Buscar Últimas 3 Transações
        │
        ▼
Exibir:
- Data/Hora
- Tipo
- Valor
- Saldo Resultante
```

---

## Fluxo de Encerramento de Conta

```text
Encerrar Conta
       │
       ▼
Saldo é igual a R$ 0,00?
       │
 ┌─────┴─────┐
 │           │
Não         Sim
 │           │
 ▼           ▼
Exibir      Remover Conta
Erro         do Sistema
               │
               ▼
       Encerramento Concluído
```

---

## Fluxo do Painel Administrativo

```text
Painel ADM
     │
     ▼
Autenticação
     │
     ▼
Credenciais válidas?
 ┌── Não ──► Acesso Negado
 │
 Sim
 │
 ▼
[1] Listar Contas
[2] Configurar Taxas e Limites
[3] Patrimônio do Banco
[0] Voltar
```

