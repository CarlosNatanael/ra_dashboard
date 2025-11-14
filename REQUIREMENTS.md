## Jr. Dev Queue Management - Requirements Document

### 1. Objective

O atual processo de revisão do Jr. Dev carece de visibilidade. Os desenvolvedores Jr. não conseguem ver o status de seus envios e os revisores de código (CRs) não possuem uma ferramenta simples para gerenciar a fila de entrada.     

Este recurso visa criar um dashboard centralizado, integrado ao RAWeb (nativamente via Filament/PHP), para resolver este problema para ambos os grupos.

### 2. Target Audience

1. **Public / Jr. Developers**: Need a read-only view to see the queue.
2. **Code Reviewers (CRs)**: Need a simple admin panel to manage the queue.
3. **Admins / Moderators**: Need oversight and full control over the panel and its users.

### 3. Core Features (Phase 1)

This describes the minimum viable product (MVP), based on the working Python prototype.

**3. 1. Public-Facing Queue (A "Visão Pública")**
A new public page on RAWeb (eg. `ra.org/reviews`) that is filterable and read-only.
- Shows a table of all sets currently in review `<(status != 'Approved')>`.
- Table Columns: `Game`, `Developer`, `Status`, `Claimed By`, `Last Updated`.
Filters:
   - A search box that filters by `Game` or `Developer`.
   - A "My Sets" button (for logged-in Jr. Devs) to filter by their own username.
   - A separate "History" page showing all sets with status 'Approved'.