# Gerenciamento de Fila para Devs Jr. - Proposta de Evolução

## 1. Contexto e Objetivo

Para apoiar o crescimento da comunidade e otimizar o trabalho de todos, esta proposta visa evoluir o processo de revisão de código para Desenvolvedores Jr.

**Objetivo Principal:** Construir uma ferramenta centralizada e transparente dentro do RAWeb (via Filament/PHP) para dar mais visibilidade aos Jr. Devs sobre seus envios e agilizar o gerenciamento da fila para os Revisores.

*   **Para Jr. Devs:** Responder à pergunta: "Onde está minha submissão?".
*   **Para Revisores (CRs):** Oferecer uma forma simples e eficiente de organizar e atualizar o andamento das revisões.

## 2. Público-Alvo e Benefícios

1.  **Desenvolvedores Jr. (Público):**
    *   **Benefício:** Transparência total. Poderão acompanhar o status de seus envios e ver a fila geral, reduzindo ansiedade e perguntas repetitivas.

2.  **Revisores de Código (CRs):**
    *   **Benefício:** Eficiência operacional. Um painel unificado para reivindicar, filtrar e atualizar submissões, substituindo métodos manuais e potencialmente dispersos.

3.  **Administradores e Moderadores:**
    *   **Benefício:** Controle e visibilidade macro. Acesso para gerenciar usuários e supervisionar todo o processo.

## 3. Funcionalidades Propostas - Fase 1 (MVP)

*Esta primeira fase (MVP) é baseada no protótipo Python que já está em uso, traduzindo sua funcionalidade para uma solução nativa e sustentável no RAWeb.*

### 3.1. Painel de Visão Pública

Uma nova página acessível a todos (ex: `ra.org/reviews`).

*   **O que será mostrado:** Uma tabela com todos os conjuntos **em revisão** (status diferente de "Aprovado").
*   **Colunas:**
    *   `Jogo`
    *   `Desenvolvedor`
    *   `Status`
    *   `Data de solicitação`
    *   `Reivindicado Por`
    *   `Última Atualização`
*   **Filtros e Funcionalidades:**
    *   Busca por `Jogo` ou `Desenvolvedor`.
    *   Botão "Meus Conjuntos" (para Jr. Devs logados) que filtra automaticamente para mostrar apenas os envios daquela pessoa.
    *   Link para uma página de "Histórico", mostrando todos os conjuntos já **Aprovados**.

### 3.2. Painel de Controle para Revisores (no Admin Filament)

Uma nova seção dentro do painel de administração existente do RAWeb.

*   **Quem terá acesso? (Modelo Híbrido):**
    *   **Acesso Automático:** Moderadores e Admins (``Role >= 4``).
    *   **Acesso via Permissão:** Revisores que forem adicionados manualmente a uma nova lista de permissões `CodeReviewers` (ideal para CRs com ``Role = 3``).

*   **Funcionalidades de Gerenciamento:**
    *   **Adicionar Conjunto:** Formulário simples para incluir um novo jogo na fila manualmente (com `ID do Jogo` e `Usuário do Desenvolvedor`).
    *   **Reivindicar:** Um botão para que um revisor "assine" uma revisão, associando seu nome à tarefa.
    *   **Atualizar Status:** Um menu para alterar o estado da revisão (ex: 'Pendente', 'Em Revisão', 'Aprovado').
    *   **Remover Entrada:** Para deletar um item da fila, se necessário.

## 4. Ideias Futuras & Chamada para Colaboração

A Fase 1 estabelece a base. O futuro da ferramenta, no entanto, pode ser moldado por quem a usa no dia a dia. Esta seção é um "backlog vivo" de ideias—e sua contribuição é fundamental!

**Gostaria muito de ouvir a opinião de todos: O que facilitaria ainda mais o seu fluxo de trabalho?**

### Ideias em Discussão:

*   **Gerenciamento de Revisores:** Um sub-painel para Admins gerenciarem a lista de Revisores com acesso manual.
*   **Auto-Submissão:** Um formulário para Jr. Devs logados submeterem seus próprios conjuntos, eliminando a etapa manual de adição por um revisor.
*   **Sistema de Notificações:** Alertas por e-mail ou no site para mudanças de status (ex: "Seu conjunto foi aprovado").
*   **Comentários Internos:** Um campo para que os revisores deixem notas privadas sobre uma submissão.
*   **Métricas:** Um dashboard simples com tamanho da fila e tempo médio de revisão.

---