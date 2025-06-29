from django.db import models

# Create your models here.

class FormTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    schema = models.JSONField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WorkflowDefinition(models.Model):
    form_template = models.OneToOneField(FormTemplate, on_delete=models.CASCADE)
    states = models.JSONField()  

    def __str__(self):
        return f"Workflow for {self.form_template.name}"
    
class Transition(models.Model):
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE, related_name='transitions')
    from_state = models.CharField(max_length=100)
    to_state = models.CharField(max_length=100)
    allowed_roles = models.JSONField()  # e.g., ["Employee", "Manager"]

    def __str__(self):
        return f"{self.from_state} → {self.to_state}"

class FormSubmission(models.Model):
    form_template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    submitted_by = models.CharField(max_length=100)  # From JWT user info
    data = models.JSONField()  # Submitted form data
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.form_template.name} by {self.submitted_by}"

class WorkflowInstance(models.Model):
    submission = models.OneToOneField(FormSubmission, on_delete=models.CASCADE)
    current_state = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.submission.form_template.name} - {self.current_state}"
