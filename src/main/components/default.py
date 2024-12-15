from sourcetypes import django_html, javascript

from main.models import Person
from tetra import public
from tetra.components import FormComponent

from main.forms import PersonForm


class PersonFormComponent(FormComponent):
    form_class = PersonForm

    def load(self, *args, **kwargs) -> None:
        self.persons = Person.objects.all()
        self.message: str = ""

    @public
    def remove(self, id: int) -> None:
        person = Person.objects.get(id=id)
        person.delete()
        self.message = f"Person {person} successfully deleted."

    def form_valid(self, form) -> None:
        instance = form.save(commit=False)
        instance.save()
        self.message = "Person successfully saved."
        self.persons = Person.objects.all()
        self.clear()

    def form_invalid(self, form) -> None:
        self.message = "Error saving person."

    # language=html
    template: django_html = """
    <div class='card'>
        <h3 class='card-title'>Create a new Person:</h3>
        {% csrf_token %}
        
        {{ form }}
        <button type='submit' @click='submit()'>Submit</button>    
    
        <p><strong>Alpine.js:</strong> first_name: {% @v 'first_name' %}, last_name: 
        {% @v 'last_name' %}</p>
        <p><strong>Django:</strong> first_name: {{first_name}}, last_name: 
        {{last_name}}</p>
        <p>Attachment: {{attachment}}<br/>
        {% if attachment %}
        <img src='{{attachment.path}}' alt='uploaded picture'>
        {% endif %}
        </p>
        <h4>Persons:</h4>
        <ul>
        {% for person in persons %}
          <li>
          {{person}}
          {% if person.attachment %}
          Attachment: {{person.attachment}}
          {% endif %}
          <button @click='remove({{person.id}})'>X</button>
          </li>
        {% endfor %}
        </ul>
        {{message}}
    </div>
    """

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
