# Django Workflow Management System

A Django REST API that supports both **sequential** and **parallel** workflow management with role-based approvals.

## 🚀 Features

### ✅ Parallel Workflow Support

- **Multiple simultaneous approvals** required before state transition
- **Role-based approval tracking** with individual approver records
- **Flexible approval criteria** (all roles, any role, specific count)
- **Real-time status tracking** of pending and completed approvals

### ✅ Sequential Workflow Support

- **Traditional step-by-step** workflow progression
- **Single approval** moves to next state
- **Backward compatibility** with existing workflows

### ✅ Security & Authentication

- **Keycloak JWT integration** for authentication
- **Role-based access control** (RBAC)
- **Audit trail** of all approvals and transitions

## 🏗️ Architecture

### Database Models

```python
FormTemplate → WorkflowDefinition → Transition
     ↓              ↓                ↓
FormSubmission → WorkflowInstance → Approval
```

### Key Components

1. **FormTemplate**: Defines form structure and validation rules
2. **WorkflowDefinition**: Defines workflow states and transitions
3. **Transition**: Maps state transitions with approval requirements
4. **FormSubmission**: Stores submitted form data
5. **WorkflowInstance**: Tracks active workflow instances
6. **Approval**: Records individual approvals with status and metadata

## 🔄 Workflow Types

### Sequential Workflow

```
Form → [Manager] → [HR] → [Finance] → Approved
```

- **One approval** moves to next state
- **Linear progression** through states
- **Immediate transition** after approval

### Parallel Workflow

```
Form → [Manager + HR] → [Finance] → Approved
       ↓     ↓
   (Parallel) (Parallel)
```

- **Multiple approvals** required simultaneously
- **Configurable approval count** (e.g., 2 out of 3 roles)
- **State transition** only after all required approvals

## 📋 API Endpoints

### Form Management

- `POST /api/form-template/` - Create form templates (Admin only)
- `POST /api/workflow-definition/` - Define workflows (Admin only)

### Workflow Operations

- `POST /api/submit-form/` - Submit forms and start workflow
- `POST /api/approve-workflow/` - Approve/reject workflow transitions
- `GET /api/workflow-status/<id>/` - Get workflow status and approvals

## 🛠️ Setup & Installation

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

## 📝 Usage Examples

### 1. Create a Parallel Workflow

```json
POST /api/workflow-definition/
{
    "form_template": 1,
    "states": ["Draft", "Manager_HR_Review", "Finance_Review", "Approved"],
    "transitions": [
        {
            "from_state": "Draft",
            "to_state": "Manager_HR_Review",
            "allowed_roles": ["Manager", "HR"],
            "transition_type": "parallel",
            "required_approvals": 2,
            "approval_criteria": {"all_roles": true}
        },
        {
            "from_state": "Manager_HR_Review",
            "to_state": "Finance_Review",
            "allowed_roles": ["Finance"],
            "transition_type": "sequential",
            "required_approvals": 1
        },
        {
            "from_state": "Finance_Review",
            "to_state": "Approved",
            "allowed_roles": ["Finance"],
            "transition_type": "sequential",
            "required_approvals": 1
        }
    ]
}
```

### 2. Submit a Form

```json
POST /api/submit-form/
{
    "form_template": 1,
    "data": {
        "employee_name": "John Doe",
        "request_amount": 5000,
        "reason": "Training expenses"
    }
}
```

### 3. Approve Workflow

```json
POST /api/approve-workflow/
{
    "submission_id": 1,
    "action": "approve",
    "comments": "Approved after review"
}
```

### 4. Check Workflow Status

```json
GET /api/workflow-status/1/
```

Response:

```json
{
  "id": 1,
  "current_state": "Manager_HR_Review",
  "is_completed": false,
  "pending_approvals": [
    { "approver_role": "Manager", "transition__to_state": "Finance_Review" },
    { "approver_role": "HR", "transition__to_state": "Finance_Review" }
  ],
  "completed_approvals": [
    {
      "approver_role": "Manager",
      "approver_username": "manager1",
      "approved_at": "2024-01-15T10:30:00Z"
    }
  ],
  "can_transition": false
}
```

## 🔐 Authentication

The system uses Keycloak JWT tokens for authentication. Include the token in request headers:

```
Authorization: Bearer <your-jwt-token>
```

### Required Roles

- **Admin**: Create templates and workflows
- **Manager**: Approve manager-level requests
- **HR**: Approve HR-related requests
- **Finance**: Approve financial requests

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 Database Schema

### Key Relationships

- `FormTemplate` ↔ `WorkflowDefinition` (One-to-One)
- `WorkflowDefinition` ↔ `Transition` (One-to-Many)
- `FormSubmission` ↔ `WorkflowInstance` (One-to-One)
- `WorkflowInstance` ↔ `Approval` (One-to-Many)

### Approval Tracking

- **Status**: pending, approved, rejected
- **Approver metadata**: role, username, timestamp, comments
- **Transition linkage**: tracks which transition was approved

## 🚨 Important Notes

### Parallel Workflow Behavior

1. **Multiple approvals** are created when workflow starts
2. **State transition** only occurs when required approval count is met
3. **Partial approvals** are tracked and displayed
4. **Rejection** immediately stops the workflow

### Security Considerations

1. **Role validation** on every approval request
2. **Atomic transactions** prevent race conditions
3. **Audit trail** of all approvals and transitions
4. **JWT token validation** on all endpoints

## 🔧 Customization

### Adding New Workflow Types

1. Extend `Transition` model with new `transition_type`
2. Update approval logic in `approve_workflow` view
3. Add corresponding serializers and validators

### Custom Approval Criteria

Modify `approval_criteria` JSON field to support:

- Percentage-based approvals
- Time-based approvals
- Conditional approvals based on form data

## 📞 Support

For issues and questions:

1. Check the API documentation
2. Review the test cases
3. Check the workflow status endpoint for debugging
4. Verify Keycloak configuration and roles

## 🎯 Future Enhancements

- [ ] Email notifications for pending approvals
- [ ] Workflow templates and cloning
- [ ] Advanced approval criteria (timeouts, escalations)
- [ ] Workflow analytics and reporting
- [ ] Mobile-friendly approval interface
