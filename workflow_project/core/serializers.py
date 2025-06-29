from rest_framework import serializers
from .models import FormTemplate, WorkflowDefinition, Transition, FormSubmission, WorkflowInstance

class FormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = ['id', 'name', 'schema', 'created_at']

class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = ['id', 'from_state', 'to_state', 'allowed_roles']

class WorkflowDefinitionSerializer(serializers.ModelSerializer):
    transitions = TransitionSerializer(many=True)

    class Meta:
        model = WorkflowDefinition
        fields = ['id', 'form_template', 'states', 'transitions']

    def create(self, validated_data):
        transitions_data = validated_data.pop('transitions')
        workflow = WorkflowDefinition.objects.create(**validated_data)
        for trans_data in transitions_data:
            Transition.objects.create(workflow=workflow, **trans_data)
        return workflow

class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSubmission
        fields = ['id', 'form_template', 'submitted_by', 'data', 'submitted_at']

class WorkflowInstanceSerializer(serializers.ModelSerializer):
    submission = FormSubmissionSerializer()

    class Meta:
        model = WorkflowInstance
        fields = ['id', 'submission', 'current_state', 'updated_at']
