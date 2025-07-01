from django.urls import path
from .views import (
    create_form_template, create_workflow_definition, submit_form, transition_workflow,
    list_form_templates, list_workflows, list_user_submissions,
    list_pending_approvals, get_available_transitions, update_form_template, update_workflow_definition
)

urlpatterns = [
    path('form-template/', create_form_template, name='create_form_template'),
    path('form-template/<int:template_id>/', update_form_template, name='update_form_template'),
    path('workflow-definition/', create_workflow_definition, name='create_workflow_definition'),
    path('workflow-definition/<int:workflow_id>/', update_workflow_definition, name='update_workflow_definition'),
    path('submit-form/', submit_form, name='submit_form'),
    path('transition/', transition_workflow, name='transition_workflow'),
    path('transitions/<int:submission_id>/', get_available_transitions, name='get_available_transitions'),

    path('form-templates/', list_form_templates, name='list_form_templates'),  # Admin & Employee
    path('workflows/', list_workflows, name='list_workflows'),                  # Admin
    path('my-submissions/', list_user_submissions, name='list_user_submissions'),  # Employee
    # path('available-forms/', list_available_forms, name='list_available_forms'),   # Employee
    path('pending-approvals/', list_pending_approvals, name='list_pending_approvals'), 
]
