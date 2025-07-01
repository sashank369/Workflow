# Django Workflow Management System

## Problem Statement

Organizations often require workflows for form submissions that involve multiple steps and approvals from different roles (e.g., Manager, HR, Finance). These workflows can be sequential (one after another) or parallel (multiple approvals at the same time). There is a need for a flexible, secure, and auditable system to manage such workflows, supporting both sequential and parallel approval processes, with role-based access and real-time status tracking.

---

## Approach and Design Choices

- **Backend:** Django REST API for workflow management.
- **Frontend:** React (with role-based dashboards for Admin, Employee, Approver).
- **Authentication:** Keycloak JWT integration for secure, role-based access.
- **Workflow Engine:** Supports both sequential and parallel workflows.
  - **Sequential:** Each state requires a single approval to move forward.
  - **Parallel:** Multiple roles can approve in any order; state transitions only after all required approvals.
- **Database Models:** Modular design with entities for FormTemplate, WorkflowDefinition, Transition, FormSubmission, WorkflowInstance, and Approval.
- **Extensibility:** Easily add new workflow types or custom approval criteria.
- **Auditability:** All transitions and approvals are logged for traceability.
- **Security:** Role validation, atomic transactions, and JWT validation on all endpoints.

---

## Prerequisites

- Python 3.8+
- PostgreSQL
- Keycloak server (for authentication)
- Node.js and npm (for frontend)

---

## Frontend

- **Stack:** React, Tailwind CSS
- **Structure:**
  - Role-based dashboards for Admin, Employee, and Approver (Manager/HR)
  - Uses Axios for API requests to the Django backend
  - Handles authentication via Keycloak JWT tokens stored in localStorage
  - Modern UI with Tailwind CSS for styling
- **Setup & Run:**
  1. Navigate to `workflow-frontend` directory:
     ```bash
     cd workflow-frontend
     ```
  2. Install dependencies:
     ```bash
     npm install
     ```
  3. Start the development server:
     ```bash
     npm start
     ```
     The app will run at `http://localhost:3000` by default.
- **Interaction:**
  - The frontend communicates with the Django backend via REST API endpoints.
  - JWT tokens are included in API requests for authentication and role-based access.
  - Dashboards and available actions are determined by the user's role (decoded from the JWT).

---

## Backend API Endpoints

The backend exposes a set of REST API endpoints for managing workflows, forms, and approvals. All endpoints require authentication via Keycloak JWT, and access is controlled by user roles (Admin, Employee, Manager, HR, Finance).

### Form Management 

- `POST /api/form-template/` — Create a new form template  (Admin only)
- `PUT /api/form-template/<id>/` — Update an existing form template  (Admin only)
- `GET /api/form-templates/` — List all form templates

### Workflow Definition 

- `POST /api/workflow-definition/` — Define a new workflow (states, transitions, roles) (Admin only)
- `PUT /api/workflow-definition/<id>/` — Update an existing workflow definition  (Admin only)
- `GET /api/workflows/` — List all workflow definitions  (Admin only)

### Form Submission 

- `POST /api/submit-form/` — Submit a form to start a workflow
- `GET /api/my-submissions/` — List submissions made by the logged-in employee (Employee)

### Workflow Operations (Approvers: Manager, HR)

- `GET /api/pending-approvals/` — List workflow instances pending approval for the logged-in approver
- `GET /api/transitions/<submission_id>/` — Get available transitions for a submission (based on current state and user role)
- `POST /api/transition/` — Transition a workflow to the next state


#### How to Access

- All endpoints are under `/api/` and require the `Authorization: Bearer <your-jwt-token>` header.
- The available endpoints and actions depend on the user's role, which is determined from the JWT token.
- The frontend automatically includes the JWT in requests and shows/hides actions based on the user's role.

#### Use of Endpoints

- **Admins**: Create and manage form templates and workflow definitions.
- **Employees**: Submit forms and track their own submissions.
- **Approvers (Manager, HR, Finance)**: View and act on pending approvals, transition workflows as per their role.


---

## Installation (Backend)

```bash
# Clone repository
git clone <repository-url>
cd workflow_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
```

### Environment Configuration

Update `settings.py` with your database and Keycloak configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Authentication

Include your Keycloak JWT token in request headers:

```
Authorization: Bearer <your-jwt-token>
```

### Setup Keycloak:

- Create realm `demo-realm`
- Add client `django-backend`
- Set Web Origins → `http://localhost:3000`
- Set redirect URIs → `http://localhost:3000/*`
- Define roles: Admin, Employee, Manager, HR

## Assumptions Made

- All users and roles are managed in Keycloak; the system trusts the JWT for role validation.
- Users and roles are created by Keycloak GUI only. And there are only 3 category of roles (Admin, Approver and employee).
- And make sure password for users is "password" and make temparary password off.
- Add respective details like email, first and last name because then only user will be created completely.
- The workflow definitions (states, transitions, roles) are created by Admin users.
- The frontend and backend are run separately; CORS and API endpoints are configured accordingly.
- PostgreSQL is used as the database backend.
- The system is deployed in a secure environment where Keycloak and the Django server can communicate.
- 
