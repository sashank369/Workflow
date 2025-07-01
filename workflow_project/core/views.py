from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import (
    FormTemplate, WorkflowDefinition, FormSubmission, WorkflowInstance, Transition
)
from .serializers import (
    FormTemplateSerializer, WorkflowDefinitionSerializer,
    FormSubmissionSerializer, WorkflowInstanceSerializer, TransitionSerializer
)
from .auth.decorators import keycloak_required
from django.db.models import Q



@api_view(['POST'])
@keycloak_required(required_roles=['Admin'])  # Only Admins can create templates
def create_form_template(request):
    serializer = FormTemplateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@keycloak_required(required_roles=['Admin'])  # Only Admins can define workflows
def create_workflow_definition(request):
    serializer = WorkflowDefinitionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@keycloak_required()
def submit_form(request):
    user_info = request.user_info
    submitted_by = user_info.get("preferred_username", "anonymous")

    data = request.data.copy()
    data["submitted_by"] = submitted_by

    form_template_id = data.get("form_template")
    form_data = data.get("data", {})

  
    template = get_object_or_404(FormTemplate, id=form_template_id)
    # print(f"Form template: {template}",template.schema)  # Debugging line
  
    field_definitions = template.schema.get("fields", [])
    required_fields = [f["name"] for f in field_definitions if f.get("required")]
    print(f"Required fields: {required_fields}")  # Debugging line

    missing_fields = [field for field in required_fields if field not in form_data or not form_data[field]]
    print(f"Missing fields: {missing_fields}")  # Debugging line
    if missing_fields:
        return Response(
            {"error": f"Missing required fields: {', '.join(missing_fields)}"},
            status=400
        )

    serializer = FormSubmissionSerializer(data=data)
    if serializer.is_valid():
        submission = serializer.save()
        # print(f"Form submission created: {submission}",submission.form_template)  # Debugging line
        workflow = get_object_or_404(WorkflowDefinition, form_template=submission.form_template)
        initial_state = workflow.states[0] if workflow.states else "Draft"

        WorkflowInstance.objects.create(submission=submission, current_state=initial_state)

        return Response({"message": "Form submitted", "submission_id": submission.id}, status=201)
    print("Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=400)



@api_view(['POST'])
@keycloak_required()
def transition_workflow(request):
    submission_id = request.data.get("submission_id")
    target_state = request.data.get("next_state")
    user_roles = request.user_info.get("realm_access", {}).get("roles", [])
    username = request.user_info.get("preferred_username")

    instance = get_object_or_404(WorkflowInstance, submission_id=submission_id)
    current_state = instance.current_state
    workflow = get_object_or_404(WorkflowDefinition, form_template=instance.submission.form_template)

    transition = workflow.transitions.filter(from_state=current_state, to_state=target_state).first()
    if not transition:
        return Response({"error": "Invalid transition"}, status=400)

    allowed_roles = transition.allowed_roles
    logical_type = transition.logical_type.upper()

    if not any(role in user_roles for role in allowed_roles):
        return Response({"error": "Permission denied. Role not allowed."}, status=403)

    # If transition already done
    if instance.current_state != current_state:
        return Response({"message": "Transition already completed by another role."}, status=403)

    approvals = instance.partial_approvals.get(target_state, [])
    if username in approvals:
        return Response({"message": "You have already approved this transition."}, status=200)

    approvals.append(username)
    instance.partial_approvals[target_state] = approvals

    if logical_type == "AND":
        role_approvers = [role for role in allowed_roles if any(role in user_roles for role in allowed_roles)]
        if len(approvals) >= len(set(allowed_roles)):
            instance.current_state = target_state
            instance.partial_approvals.pop(target_state)
    else:  # OR
        instance.current_state = target_state
        instance.partial_approvals.pop(target_state)

    instance.save()
    return Response({"message": f"Transitioned to {instance.current_state}"}, status=200)


@api_view(['GET'])
@keycloak_required()
def list_form_templates(request):
    templates = FormTemplate.objects.all()
    serializer = FormTemplateSerializer(templates, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@keycloak_required(required_roles=['Admin'])
def list_workflows(request):
    workflows = WorkflowDefinition.objects.all()
    serializer = WorkflowDefinitionSerializer(workflows, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@keycloak_required()
def list_user_submissions(request):
    username = request.user_info.get("preferred_username")
    instances = WorkflowInstance.objects.filter(submission__submitted_by=username)
    serializer = WorkflowInstanceSerializer(instances, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# @keycloak_required()
# def list_available_forms(request):
#     templates = FormTemplate.objects.all()
#     serializer = FormTemplateSerializer(templates, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
@keycloak_required()
def list_pending_approvals(request):
    user_roles = request.user_info.get("realm_access", {}).get("roles", [])
    pending_instances = []

    for instance in WorkflowInstance.objects.all():
        workflow = get_object_or_404(WorkflowDefinition, form_template=instance.submission.form_template)
        transitions = workflow.transitions.filter(from_state=instance.current_state)

        for t in transitions:
            if any(role in user_roles for role in t.allowed_roles):
                pending_instances.append(instance)
                break

    serializer = WorkflowInstanceSerializer(pending_instances, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@keycloak_required()
def get_available_transitions(request, submission_id):
    user_roles = request.user_info.get("realm_access", {}).get("roles", [])
    
    # Get the workflow instance
    instance = get_object_or_404(WorkflowInstance, submission_id=submission_id)
    workflow = get_object_or_404(WorkflowDefinition, form_template=instance.submission.form_template)
    
    # Get all possible transitions from current state
    transitions = workflow.transitions.filter(from_state=instance.current_state)
    
    # Filter transitions based on user roles
    available_transitions = []
    for transition in transitions:
        if any(role in user_roles for role in transition.allowed_roles):
            available_transitions.append({
                'from_state': transition.from_state,
                'to_state': transition.to_state,
                'allowed_roles': transition.allowed_roles,
                'logical_type': transition.logical_type
            })
    
    return Response(available_transitions)

@api_view(['PUT'])
@keycloak_required(required_roles=['Admin'])
def update_form_template(request, template_id):
    template = get_object_or_404(FormTemplate, id=template_id)
    serializer = FormTemplateSerializer(template, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@keycloak_required(required_roles=['Admin'])
def update_workflow_definition(request, workflow_id):
    workflow = get_object_or_404(WorkflowDefinition, id=workflow_id)
    transitions_data = request.data.pop('transitions', None)
    serializer = WorkflowDefinitionSerializer(workflow, data=request.data, partial=True)
    if serializer.is_valid():
        workflow = serializer.save()
        if transitions_data is not None:
            # Remove old transitions
            workflow.transitions.all().delete()
            # Add new transitions
            for trans_data in transitions_data:
                Transition.objects.create(workflow=workflow, **trans_data)
        return Response(WorkflowDefinitionSerializer(workflow).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
