from main.models import Person
from tetra import public
from tetra.components import FormComponent

from main.forms import PersonForm
import logging

logger = logging.getLogger(__name__)


class PersonFormComponent(FormComponent):
    form_class = PersonForm
    message: str = ""

    def load(self, *args, **kwargs) -> None:
        self.persons = Person.objects.all()
        self.first_name = "John"
        self.last_name = "Doe"
        self.group = None
        self.terms_conditions = True

    @public
    def remove(self, id: int) -> None:
        person = Person.objects.get(id=id)
        person.delete()
        self.message = f"Person {person} successfully deleted."

    def form_valid(self, form) -> None:
        # from tetra.utils import TetraTemporaryUploadedFile
        # file: TetraTemporaryUploadedFile = form.cleaned_data["attachment"]
        instance = form.save()
        self.message = f"Person '{instance}' successfully saved."
        self.persons = Person.objects.all()
        self._reset()

    def form_invalid(self, form) -> None:
        self.message = "Form is invalid."
