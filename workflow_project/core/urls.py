from django.urls import path
from .views import create_form_template, create_workflow_definition, submit_form, transition_workflow

urlpatterns = [
    path('form-template/', create_form_template, name='create_form_template'),
    path('workflow-definition/', create_workflow_definition, name='create_workflow_definition'),
    path('submit-form/', submit_form, name='submit_form'),
    path('transition/', transition_workflow, name='transition_workflow'),
]
