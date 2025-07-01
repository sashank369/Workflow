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

## Setup or Run Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL
- Keycloak server (for authentication)

### Installation

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

### Testing

```bash
python manage.py test
# or with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Assumptions Made

- All users and roles are managed in Keycloak; the system trusts the JWT for role validation.
- The workflow definitions (states, transitions, roles) are created by Admin users.
- The frontend and backend are run separately; CORS and API endpoints are configured accordingly.
- PostgreSQL is used as the database backend.
- The system is deployed in a secure environment where Keycloak and the Django server can communicate.
- Email notifications, advanced analytics, and mobile support are planned as future enhancements.
