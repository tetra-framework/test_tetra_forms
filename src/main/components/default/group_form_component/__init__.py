from tetra.components import ModelFormComponent
from django.contrib.auth.models import Group


class GroupFormComponent(ModelFormComponent):
    model = Group
    fields = ["id", "name"]
