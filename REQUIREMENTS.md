# Jr. Dev Queue Management - Requirements Document

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

**3.2. Admin Panel (A "Visão de Admin" no Filament)**
A new section within the existing RAWeb Filament admin panel.

- **Authorization**: Access is granted based on a hybrid logic:
1. **Automatic**: User has `Role >= 4` (Moderator or Admin).
2. **Manual**: User is in a new `CodeReviewers` permissions list (to manually add CRs who might only have `Role = 3`).

- **Features**: A table view of the same queue, but with management buttons:
   - **Add New Set**: A form to add a new game to the queue (Fields: Game ID, Developer Username).
   - **Claim Set**: A "Claim" button that assigns the CR's username to the entry.
   - **Update Status**: A dropdown/button on each entry to change the `Status` (eg. 'Pending', 'In Review', 'Approved').
   - **Delete Entry**: A button to remove the entry.

### 4. Future Ideas (Phase 2)
- **CR User Management**: A panel (visível apenas para `Role >= 4`) to add/remove users from the "Manual CR Access" list (de 3.2).
- **Jr. Dev Submission Form**: A simple form for logged-in Jr. Devs to submit their own sets to the queue automatically.