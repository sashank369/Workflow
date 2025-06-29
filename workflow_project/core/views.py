from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FormTemplate, WorkflowDefinition, FormSubmission, WorkflowInstance, WorkflowDefinition
from .serializers import FormTemplateSerializer, WorkflowDefinitionSerializer, FormSubmissionSerializer
from .auth.decorators import keycloak_required
from django.shortcuts import get_object_or_404


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

        workflow = get_object_or_404(WorkflowDefinition, form_template=submission.form_template)
        initial_state = workflow.states[0] if workflow.states else "Draft"

        WorkflowInstance.objects.create(submission=submission, current_state=initial_state)

        return Response({"message": "Form submitted", "submission_id": submission.id}, status=201)

    return Response(serializer.errors, status=400)



@api_view(['POST'])
@keycloak_required()
def transition_workflow(request):
    submission_id = request.data.get("submission_id")
    target_state = request.data.get("next_state")
    user_roles = request.user_info.get("realm_access", {}).get("roles", [])

    instance = get_object_or_404(WorkflowInstance, submission_id=submission_id)
    current_state = instance.current_state
    workflow = get_object_or_404(WorkflowDefinition, form_template=instance.submission.form_template)

    # Find valid transition
    transition = workflow.transitions.filter(from_state=current_state, to_state=target_state).first()
    if not transition:
        return Response({"error": "Invalid transition"}, status=400)

    if not any(role in user_roles for role in transition.allowed_roles):
        return Response({"error": "Permission denied. Role not allowed."}, status=403)

    instance.current_state = target_state
    instance.save()

    return Response({"message": f"Transitioned to {target_state}"}, status=200)
