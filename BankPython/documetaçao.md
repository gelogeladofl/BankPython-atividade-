# Documentação Técnica de Sistema: BankPython (Versão 2.0)

## 1. Introdução

### 1.1 Objetivo do Sistema
O **BankPython** é um sistema de gerenciamento financeiro digital executado inteiramente em memória. Ele provê uma interface de linha de comando (CLI) robusta para operações bancárias correntes, aplicando regras rígidas de validação cadastral, limites de segurança temporais, tarifação operacional e ferramentas de auditoria administrativa.

### 1.2 Escopo Atualizado
O sistema contempla em seu escopo funcional:
* **Cadastro de contas:** validação cadastral de CPF e bloqueio de datas de nascimento no futuro;
* **Controle de depósitos:** teto inicial de saldo e amortização de passivos;
* **Sistema de saques:** dupla validação temporal (limites diários e mensais) e tarifas operacionais fixas;
* **Painel administrativo:** autenticação, parametrização global e ajuste fino de limites por conta específica;
* **Módulo institucional:** consulta pública de tarifas vigentes com interface estilizada.

---

## 2. Visão Geral da Arquitetura

O sistema adota uma arquitetura modular centralizada em uma estrutura de dados global em memória RAM, segmentada em quatro macro-módulos:

```text
                               ┌────────────────────────────────┐
                               │   Interface CLI (Menu Principal)│
                               └───────────────┬────────────────┘
                                               │
         ┌────────────────────────┬────────────┴────────────┬────────────────────────┐
         ▼                        ▼                         ▼                        ▼
┌─────────────────┐      ┌─────────────────┐       ┌─────────────────┐      ┌─────────────────┐
│  Gestão Conta   │      │ Fluxo Financeiro│       │  Painel ADM     │      │   Módulo Info   │
│ ∙ Valida CPF    │      │ ∙ Saque + Taxa  │       │ ∙ Ajuste Limite │      │ ∙ Exibição das  │
│ ∙ Data Passada  │      │ ∙ Depósito      │       │ ∙ Auditoria     │      │   Tarifas com   │
│ ∙ Teto Inicial  │      │ ∙ Limite Tempo  │       │ ∙ Patrimônio    │      │   Moldura '▓'   │
└─────────────────┘      └─────────────────┘       └─────────────────┘      └─────────────────┘

```

---

## 3. Histórias de Usuário (User Stories)

### US-01 — Abertura de Conta com Proteção de Lastro

**Como** cliente bancário,

**Quero** abrir uma conta corrente digital informando meus dados validados,

**Para** garantir que minha conta seja criada de acordo com as normas de conformidade do banco.

#### Critérios de Aceitação:

* O sistema deve validar matematicamente os dígitos verificadores do CPF.
* A data de nascimento deve obrigatoriamente pertencer ao passado ou ao dia corrente.
* O saldo inicial não pode exceder o teto regulatório de **R$ 10.000,00**.
* O limite inicial do cheque especial não pode exceder o teto de **R$ 5.000,00**.

### US-02 — Realizar Saque com Trava Temporal e Tarifação

**Como** cliente bancário,

**Quero** sacar recursos da minha conta corrente,

**Para** utilizar o dinheiro em espécie respeitando meus limites de segurança.

#### Critérios de Aceitação:

* Cada saque deduz uma taxa operacional fixa de **R$ 2,50** (parametrizável).
* O sistema deve acumular as operações do dia corrente e impedir o saque se o montante diário ultrapassar **R$ 1.000,00**.
* O sistema deve acumular as operações do mês corrente e impedir o saque se o montante mensal ultrapassar **R$ 5.000,00**.
* O cálculo deve considerar o Horário Oficial de Brasília (**UTC-3**) para evitar fraudes de relógio.

### US-03 — Gestão de Limite Customizado (Painel ADM)

**Como** administrador do sistema,

**Quero** acessar um painel autenticado e alterar o cheque especial de uma conta específica,

**Para** conceder limites maiores a clientes selecionados sem alterar a regra global de novas contas.

#### Critérios de Aceitação:

* Exigir usuário (`lucas`) e senha (`123`).
* Permitir a busca de uma conta ativa via CPF.
* Atualizar o limite de cheque especial especificamente para a conta selecionada e registrar o evento no extrato do cliente para fins de auditoria.

---

## 4. Requisitos do Sistema

### 4.1 Requisitos Funcionais (RF)

* **SYS-RF-01 (Abertura de Conta Corrente):** O sistema deve cadastrar contas sob a chave de um CPF válido e único, exigindo data de nascimento passada, saldo inicial ($\le$ R$ 10.000,00) e limite de cheque especial ($\le$ R$ 5.000,00).
* **SYS-RF-02 (Validação Temporal de Saques):** O sistema deve varrer o histórico da conta nas janelas diárias e mensais antes de autorizar um novo débito de saque.
* **SYS-RF-03 (Consulta de Extrato Estendida):** O sistema deve exibir de forma decrescente as últimas 5 movimentações reais da conta corrente.
* **SYS-RF-04 (Alteração de Parâmetro por Conta Alvo):** O painel administrativo deve isolar e modificar o limite de cheque especial de um CPF específico sem impactar o teto global de novas contas.
* **SYS-RF-05 (Painel Institucional Transparente):** O sistema deve exibir de forma clara todas as taxas e limites máximos em vigor, acessível publicamente sem autenticação.

### 4.2 Regras de Negócio (Business Rules)

As Regras de Negócio definem as restrições, cálculos e comportamentos operacionais inflexíveis do sistema BankPython. Qualquer alteração de código deve, obrigatoriamente, respeitar as diretrizes abaixo.

#### SYS-RN-01 — Invariante de Saldo e Limite para Saques

Toda e qualquer tentativa de saque solicitada pelo cliente passará por uma validação matemática de fundos. A soma do valor solicitado com a taxa de saque não pode ultrapassar o patrimônio líquido imediatamente disponível da conta (saldo real + limite de crédito).

$$Valor_{\text{Saque}} + Taxa_{\text{Operacional}} \le Saldo_{\text{Atual}} + Limite_{\text{ChequeEspecial}}$$

* **Comportamento:** Se a equação for falsa, o sistema aborta a transação e exibe uma mensagem de saldo insuficiente.

#### SYS-RN-02 — Tarifação Operacional Compulsória

Todo saque autorizado pelo sistema sofrerá a incidência imediata de uma tarifa operacional fixa, atualmente estipulada em **R$ 2,50**.

* **Gatilho:** Aplicada no exato momento do débito do saque.
* **Isolamento:** O valor deve ser lido da variável global parametrizada, permitindo que o Administrador altere a taxa globalmente sem quebrar o fluxo.

#### SYS-RN-03 — Sincronização Cronológica (Fuso Horário de Brasília)

Para mitigar fraudes baseadas em manipulação de relógios locais (do lado do cliente) ou inconsistências de fuso horário em servidores de nuvem, todas as operações de validação de datas e registros de transações devem utilizar o fuso horário oficial de Brasília: **UTC-3**.

#### SYS-RN-04 — Algoritmo de Validação Coercitiva de CPF

O sistema não aceitará strings genéricas no campo de identificação fiscal. O CPF informado na abertura da conta deve passar por uma esteira de três validações:

* **Limpeza de caracteres:** Remoção de pontos, traços ou espaços.
* **Bloqueio de sequências falsas:** Rejeição de strings com 11 dígitos idênticos (Ex: `111.111.111-11`).
* **Módulo 11:** Validação matemática dos dois dígitos verificadores (DV) com base nos 9 primeiros números.

#### SYS-RN-05 — Proteção de Validação Cronológica (Idade/Nascimento)

No ato da abertura de conta, a data de nascimento do titular é convertida em um objeto temporal e comparada estritamente com a data atual fornecida pela SYS-RN-03.

$$Data_{\text{Nascimento}} \le Data_{\text{Hoje}}$$

* **Restrição:** O sistema bloqueará o avanço do cadastro se a data informada for posterior ao dia de hoje.

#### SYS-RN-06 — Teto de Aporte Inicial (Garantia de Lastro)

Como medida de segurança contra lavagem de dinheiro ou erros de digitação grosseiros no ambiente CLI, o saldo inicial depositado no momento da abertura da conta é limitado ao valor máximo de **R$ 10.000,00**.

* **Comportamento:** O sistema rejeita valores negativos e valores superiores a R$ 10.000,00.

#### SYS-RN-07 — Teto do Limite Inicial de Cheque Especial

O crédito pré-aprovado fornecido automaticamente para novas contas criadas por usuários comuns possui um limite regulatório máximo intransponível de **R$ 5.000,00**.

* **Exceção:** Este limite aplica-se estritamente à função de criação de conta comum (`abrir_conta`), não limitando as ações diretas do Painel Administrativo.

#### SYS-RN-08 — Trava Temporal de Segurança (Limites de Saque)

Antes de autorizar a saída de capital via saque, o sistema varre o histórico (extrato) da conta ativa para calcular o comportamento financeiro do cliente em duas janelas temporais móveis:

* **Janela Diária:** A soma de todos os saques com data igual à data atual não pode exceder **R$ 1.000,00**.
* **Janela Mensal:** A soma de todos os saques com mês e ano iguais ao mês/ano atual não pode exceder **R$ 5.000,00**.

#### SYS-RN-09 — Amortização Automática de Passivos

Caso a conta do cliente esteja operando com o saldo negativo (utilizando o Cheque Especial), qualquer entrada financeira oriunda da função de Depósito será utilizada prioritariamente para cobrir o saldo devedor.

* **Exemplo:** Se a conta possui saldo de -R$ 200,00 e o cliente deposita R$ 500,00, o saldo final resultante será ajustado de forma transparente para +R$ 300,00, liberando o limite do cheque especial de volta ao seu estado original de repouso.

#### SYS-RN-10 — Elegibilidade para Encerramento de Conta

O encerramento lógico de uma conta corrente exige a neutralidade patrimonial absoluta do cliente com a instituição financeira, ou seja, o **Saldo Atual deve ser igual a R$ 0,00**.

* **Bloqueio Positivo:** Se houver saldo remanescente, a conta não pode ser apagada (o cliente deve sacar ou transferir o valor).
* **Bloqueio Negativo:** Se houver utilização ativa do cheque especial, a exclusão é vetada até que o cliente realize um depósito compensatório.

#### SYS-RN-11 — Hierarquia de Crédito (Privilégio do Administrador)

O Painel Administrativo autenticado detém soberania sobre os parâmetros individuais das contas. O Administrador do sistema pode buscar qualquer CPF ativo e definir um novo limite de Cheque Especial sem obedecer ao teto da SYS-RN-07.

* **Auditoria:** Toda alteração manual de limite realizada pelo Administrador deve injetar uma transação fictícia de valor zero (R$ 0,00) no extrato do cliente para rastreabilidade de auditoria interna, documentando o novo limite conhecido.

### 4.3 Requisitos Não Funcionais (RNF)

* **SYS-RNF-01 (Robustez de Entrada):** O sistema deve interceptar falhas do tipo `ValueError` em qualquer entrada de dados via console e reiniciar a coleta de dados sem derrubar o processo.
* **SYS-RNF-02 (Estilo e Padronização Visual):** Telas de visualização institucional ou menus estruturados devem utilizar o caractere denso `▓` para delimitação de caixas de texto.

---

## 5. Matriz de Rastreabilidade Atualizada

| ID Requisito | Regra Associada | Sprint | Objetivo de Verificação |
| --- | --- | --- | --- |
| **SYS-RF-01** | SYS-RN-03 / SYS-RN-04 | Sprint 1 | Validar CPF matemático e bloquear saldo inicial > R$ 10k |
| **SYS-RF-02** | SYS-RN-01 / SYS-RN-02 | Sprint 2 | Somar saques do dia/mês no fuso UTC-3 e aplicar taxa de R$ 2,50 |
| **SYS-RF-04** | N/A | Sprint 3 | Modificar limite de cheque especial de conta específica via ADM |
| **SYS-RF-05** | SYS-RNF-02 | Sprint 3 | Renderizar tela de tarifas envelopada em blocos ▓ |

---

## 6. Fluxogramas e Protótipos de Processo (CLI)

### 6.1 Fluxo Atualizado de Abertura de Conta

```text
[Menu Opção 1] ──► Digitar CPF ──► Validação Algorítmica (Módulo 11)
                                      │
                                      ├──► Inválido/Duplicado ──► Retorna Erro
                                      └──► Válido ──► Digitar Data Nasc.
                                                        │
    ┌───────────────────────────────────────────────────┘
    ▼
Validar se Data > Hoje (Brasília) ──► Sim ──► Retorna Erro
    │
    └──► Não ──► Coletar Saldo Inicial (Max R$ 10.000,00)
                   │
                   └──► Coletar Limite Especial (Max R$ 5.000,00) ──► Conta Criada!

```

### 6.2 Visualização da Interface Institucional (Opção 4)

```text
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                    ▓
▓                  INFORMAÇÕES E TARIFAS VIGENTES                    ▓
▓                                                                    ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                    ▓
▓ - Tarifa de Saque por Operação: R$ 2.50                            ▓
▓ - Limite de Saque Diário: R$ 1000.00                               ▓
▓ - Limite de Saque Mensal: R$ 5000.00                               ▓
▓ - Cheque Especial Máximo Inicial: R$ 5000.00                       ▓
▓ - Saldo Inicial Máximo Permitido: R$ 10000.00                      ▓
▓                                                                    ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

```

### 6.3 Fluxo Administrativo de Ajuste Fino de Conta Específica

```text
[Painel ADM -> Opção 3] ──► Solicitar CPF Alvo
                               │
                               ├──► Não Existe ──► Retorna Erro
                               └──► Existe ──► Exibe Limite Atual
                                                  │
                                                  ▼
                                       Inserir Novo Limite (Float)
                                                  │
                                                  ▼
                                       Grava dado no CPF informado
                                       & Registra Transação de Auditoria

```
