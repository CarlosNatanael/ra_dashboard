# Jr. Dev Queue Management - Evolution Proposal

## 1. Context and Objective

To support community growth and optimize everyone's workflow, this proposal aims to evolve the code review process for Jr. Developers.

**Main Objective:** To build a centralized and transparent tool within RAWeb (via Filament/PHP) to give Jr. Devs more visibility into their submissions and streamline queue management for Reviewers.

* **For Jr. Devs:** Answer the question: "Where is my submission?".
* **For Reviewers (CRs):** Provide a simple and efficient way to organize and update the progress of reviews.

## 2. Target Audience and Benefits

1.  **Jr. Developers (Public):**
    * **Benefit:** Full transparency. They will be able to track the status of their submissions and see the general queue, reducing anxiety and repetitive questions.

2.  **Code Reviewers (CRs):**
    * **Benefit:** Operational efficiency. A unified dashboard to claim, filter, and update submissions, replacing manual and potentially scattered methods.

3.  **Administrators and Moderators:**
    * **Benefit:** Macro control and visibility. Access to manage users and oversee the entire process.

## 3. Proposed Features - Phase 1 (MVP)

*This first phase (MVP) is based on the Python prototype already in use, translating its functionality into a native and sustainable solution on RAWeb.*

### 3.1. Public View Dashboard

A new page accessible to everyone (e.g., `ra.org/reviews`).

* **What it will show:** A table with all sets **under review** (status other than "Approved").
* **Columns:**
    * `Game`
    * `Developer`
    * `Status`
    * `Request Date`
    * `Claimed By`
    * `Last Update`
* **Filters and Features:**
    * Search by `Game` or `Developer`.
    * "My Sets" button (for logged-in Jr. Devs) that automatically filters to show only that person's submissions.
    * Link to a "History" page, showing all sets already **Approved**.

### 3.2. Control Panel for Reviewers (in Filament Admin)

A new section within the existing RAWeb admin panel.

* **Who will have access? (Hybrid Model):**
    * **Automatic Access:** Moderators and Admins (``Role >= 4``).
    * **Permission-Based Access:** Reviewers who are manually added to a new `CodeReviewers` permission list (ideal for CRs with ``Role = 3``).

* **Management Features:**
    * **Add Set:** Simple form to manually add a new game to the queue (with `Game ID` and `Developer User`).
    * **Claim:** A button for a reviewer to "sign up" for a review, associating their name with the task.
    * **Update Status:** A menu to change the review's state (e.g., 'Pending', 'In Review', 'Approved').
    * **Remove Entry:** To delete an item from the queue, if necessary.

## 4. Future Ideas & Call for Collaboration

Phase 1 lays the foundation. The tool's future, however, can be shaped by those who use it daily. This section is a "living backlog" of ideas—and your contribution is essential!

**I would love to hear everyone's opinion: What would make your workflow even easier?**

### Ideas Under Discussion:

* **Reviewer Management:** A sub-panel for Admins to manage the list of manually-added Reviewers.
* **Self-Submission:** A form for logged-in Jr. Devs to submit their own sets, eliminating the manual addition step by a reviewer.
* **Notification System:** Email or site alerts for status changes (e.g., "Your set has been approved").
* **Internal Comments:** A field for reviewers to leave private notes on a submission.
* **Metrics:** A simple dashboard with queue size and average review time.

---