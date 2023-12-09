from rest_framework import serializers
from .models import Todo, Step, Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'title']

class StatusPkField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        return int(data)

class StepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    status_id = StatusPkField(many=False, queryset=Status.objects.all())
    class Meta:
        model = Step
        depth = 1
        fields = ['id','name','days','status','status_id']

class TodoSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    status_options = serializers.SerializerMethodField()
    class Meta:
        model = Todo
        depth = 1
        fields = ('id', 'title', 'description', 'completed','steps','status_options')

    def get_status_options(self, obj):
        # Retrieve and serialize the status options
        status_options = Status.objects.all()
        return StatusSerializer(status_options, many=True).data

    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        instance = Todo.objects.create(**validated_data)
        for step_data in steps_data:
            Step.objects.create(todo=instance, **step_data)
        return instance

    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', [])
        instance = super(TodoSerializer,self).update(instance, validated_data)

        # Track the IDs of steps to be deleted
        steps_with_ids = set(step_data.get('id') for step_data in steps_data if 'id' in step_data)

        # Delete steps that are not present in the updated data
        instance.steps.exclude(id__in=steps_with_ids).delete()

        # Update or create each step
        for step_data in steps_data:
            step_id = step_data.get('id', None)
            # Get all fields except 'id' and foreign key for Step model
            step_fields = [field.attname for field in Step._meta.get_fields() if field.attname !='id' and field.attname != 'todo_id']
            # Create a dictionary of default values for get_or_create
            defaults = {field: step_data.get(field, None) for field in step_fields}
            print(defaults)
            if step_id:
                step = instance.steps.filter(id=step_id).first()
                if step:
                    for field in defaults:
                        setattr(step, field, defaults[field])
                    step.save()
            else:
                Step.objects.create(todo=instance, **step_data)

        return instance