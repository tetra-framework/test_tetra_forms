from sourcetypes import django_html, javascript

from main.models import Person
from tetra import public
from tetra.components import FormComponent

from main.forms import PersonForm


class PersonFormComponent(FormComponent):
    form_class = PersonForm
    message: str = ""

    def load(self, *args, **kwargs) -> None:
        self.persons = Person.objects.all()
        self.first_name = "John"
        self.last_name = "Doe"
        # self.terms_conditions = True

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
        self.message = "Error saving person."

    # language=html

    # language=javascript
    # script: javascript = """
    # export default {
    #
    # // FIXME: this code doesn't work properly, is hardcoded and wrong.
    # // uploading files should be done in tetra.js
    # init() {
    #     document.addEventListener('DOMContentLoaded', function() {
    #       const componentContainer = document.querySelector('[tetra-component="main__default__person_form_component"]');
    #       function attachFormListener() {
    #         const form = document.getElementById('personForm');
    #         form.addEventListener('submit', function(event) {
    #           event.preventDefault();
    #           const formData = new FormData(form);
    #           fetch(form.action, {
    #             method: 'POST',
    #             body: formData,
    #             headers: {
    #               'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value,
    #               'X-Requested-With': 'XMLHttpRequest'
    #             }
    #           })
    #           .then(response => response.text())
    #           .then(html => updateComponent(html))
    #           .catch(error => console.error('Error:', error));
    #         });
    #       }
    #       function updateComponent(html) {
    #         const tempDiv = document.createElement('div');
    #         tempDiv.innerHTML = html;
    #         const newComponentContainer = tempDiv.querySelector('[tetra-component="main__default__person_form_component"]');
    #
    #         if (newComponentContainer) {
    #           componentContainer.innerHTML = newComponentContainer.innerHTML;
    #           Alpine.initTree(componentContainer);
    #           attachFormListener();
    #         } else {
    #           console.error('New component container not found in the response');
    #         }
    #       }
    #       attachFormListener();
    #     })
    #   }
    # }
    # """

    # should be done automatically in FormComponent:
    # def form_valid(self, form) -> None:
    #     self.form.save()
    #     self.message = "Person successfully saved."
    #
    # def form_invalid(self, form) -> None:
    #     self.message = "Error saving person."
