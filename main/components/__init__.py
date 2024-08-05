from sourcetypes import django_html

from main.models import Person, Book, PersonAddress
from tetra import Library, public
from tetra.components import FormComponent, FormFactory

from main.forms import PersonForm, BookForm, AddressForm
from tetra.components.base import DependencyFormMixin, ModelFormComponent

default = Library()


@default.register
class PersonFormComponent(FormComponent):
    form_class = FormFactory.factory(Form=PersonForm)

    def load(self, *args, **kwargs) -> None:
        self.persons = Person.objects.all()
        self.message: str = ""

    @public
    def remove(self, id: int) -> None:
        person = Person.objects.get(id=id)
        person.delete()
        self.message = f"Person {person} successfully deleted."
        # self.persons = Person.objects.all()

    def form_valid(self, form) -> None:
        instance = form.save(commit=False)
        instance.save()
        self.message = "Person successfully saved."
        self.persons = Person.objects.all()
        return self.render()

    def form_invalid(self, form) -> None:
        self.message = "Error saving person."
        return self.render()

    # language=html
    template = """
    <div class='card'>
       <h3 class='card-title'>Create a new Person:</h3>
        <form id="personForm" enctype="multipart/form-data" method="post">
            <input type="hidden" name="identifier" >
            {% csrf_token %}
                {% for field in form %}
                  {{field.label}}{% if field.field.required %} *{% endif %}:
                  {{field}}
                  {{field.errors}}
                {% endfor %}
             <button type='submit'>Submit</button>    
          </form>
        <p>Alpine.js: first_name: <span x-text='first_name'></span> 
        last_name: <span x-text='last_name'></span></p>
        <p>Django: first_name: {{first_name}} last_name: 
        {{last_name}}</p>
        <h4>Persons:</h4>
        <ul>
        {% for person in persons %}
          <li>
          {{person}}
          {% if person.attachment %}
            <h6>Attachment</h6>
            <a href="{{person.attachment.url}}" target='_blank'>{{person.attachment}}</a>
          {% endif %}
          <button class="btn btn-danger btn-sm" 
                @click='remove({{person.id}})'>X</button>
          </li>
        {% endfor %}
        </ul>
        {{message}}
    </div>
    
<script>
document.addEventListener('DOMContentLoaded', function() {
  const componentContainer = document.querySelector('[tetra-component="main__default__person_form_component"]');

  function attachFormListener() {
    const form = document.getElementById('personForm');
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      const formData = new FormData(form);

      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value,
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.text())
      .then(html => updateComponent(html))
      .catch(error => console.error('Error:', error));
    });
  }

  function updateComponent(html) {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    const newComponentContainer = tempDiv.querySelector('[tetra-component="main__default__person_form_component"]');
    
    if (newComponentContainer) {
      componentContainer.innerHTML = newComponentContainer.innerHTML;
      Alpine.initTree(componentContainer);
      attachFormListener();
    } else {
      console.error('New component container not found in the response');
    }
  }

  attachFormListener();
});
</script>
    """


@default.register
class BookFormComponent(DependencyFormMixin, ModelFormComponent):
    form_class = FormFactory.factory(Form=BookForm)
    field_dependencies = {"delivery_from": "author"}

    def load(self, *args, **kwargs) -> None:
        self.books = Book.objects.all()
        self.message: str = ""

    def form_valid(self, form) -> None:
        instance = form.save(commit=False)
        instance.save()
        self.message = "Book successfully saved."
        self.books = Book.objects.all()
        # self.form_submitted = False
        # self.clear()
        # print("clear form")
        return self.render()

    def form_invalid(self, form) -> None:
        self.message = "Error saving book."
        return self.render()

    def ready(self):
        super().ready()
        # Reset queryset based on current author if available
        self.update_field_queryset(
            "delivery_from", PersonAddress.objects.filter(person=self.author)
        )

    @public
    def remove(self, id: int) -> None:
        book = Book.objects.get(id=id)
        book.delete()
        self.message = f"Book {book} successfully deleted."

    @public.watch("author")
    def author_changed(self, value, old_value, attr) -> None:
        self.update_field_queryset(
            "delivery_from",
            PersonAddress.objects.filter(person=self.author),
            old_value=old_value,
        )

    # language=html
    template = """
    <div class='card'>
        <h3 class='card-title'>Create a new Book:</h3>
          <form id='BookForm' enctype="multipart/form-data" method="post">
            <input type="hidden" name="identifier" >
            {% csrf_token %}
                {% for field in form %}
                  {{field.label}}{% if field.field.required %} *{% endif %}:
                  {{field}}
                  {{field.errors}}
                {% endfor %}
             <button type='submit'>Submit</button>    
          </form>  
        <p>Alpine.js: <span x-text='name'></span> 
        ( author: <span x-text='author'></span>, 
        delivery_from: <span x-text='delivery_from'></span>, 
        color: <span x-text='color'></span>)
        </p>
        <p>Django: name: {{name}} (author: {{author}}, 
        delivery_from: {{delivery_from}}, 
        color: {{color}})</p>
        <h4>Books:</h4>
        <ul>
        {% for book in books %}
          <li>
            {{book}}
            <p>delivery from: {{book.delivery_from}}</p>
            <button class="btn btn-danger btn-sm" 
                @click='remove({{book.id}})'>X</button>
          </li>
        {% endfor %}
        </ul>
        {{message}}
    </div>
    
  <script>
 document.addEventListener('DOMContentLoaded', function() {
  const componentContainer = document.querySelector('[tetra-component="main__default__book_form_component"]');

  function attachFormListener() {
    const form = document.getElementById('BookForm');
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      const formData = new FormData(form);

      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value,
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.text())
      .then(html => updateComponent(html))
      .catch(error => console.error('Error:', error));
    });
  }

  function updateComponent(html) {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    const newComponentContainer = tempDiv.querySelector('[tetra-component="main__default__book_form_component"]');
    
    if (newComponentContainer) {
      componentContainer.innerHTML = newComponentContainer.innerHTML;
      Alpine.initTree(componentContainer);
      attachFormListener();
    } else {
      console.error('New component container not found in the response');
    }
  }

  attachFormListener();
});
</script>
    """


@default.register
class AddressFormComponent(FormComponent):
    form_class = FormFactory.factory(Form=AddressForm)

    def load(self, *args, **kwargs) -> None:
        self.address_list = PersonAddress.objects.all()
        self.message: str = ""

    def form_valid(self, form) -> None:
        instance = form.save(commit=False)
        instance.save()
        self.message = "Address successfully saved."
        self.address_list = PersonAddress.objects.all()
        return self.render()


    def form_invalid(self, form) -> None:
        self.message = "Error saving address."
        return self.render()


    @public
    def remove(self, id: int) -> None:
        address = PersonAddress.objects.get(id=id)
        address.delete()
        self.message = f"Address '{address}' successfully deleted."

    # language=html
    template: django_html = """
        <div class='card'>
        <h3 class='card-title'>Create a new Address for Person:</h3>
          <form id='AddressForm' enctype="multipart/form-data" method="post">
            <input type="hidden" name="identifier" >
            {% csrf_token %}
                {% for field in form %}
                  {{field.label}}{% if field.field.required %} *{% endif %}:
                  {{field}}
                  {{field.errors}}
                {% endfor %}
             <button type='submit'>Submit</button>    
          </form>  
        <h4>Addresses:</h4>
        <ul>
        {% for address in address_list %}
          <li>
            {{address}}
            <button class="btn btn-danger btn-sm" 
                @click='remove({{address.id}})'>X</button>
          </li>
        {% endfor %}
        </ul>
        {{message}}
    </div>
    <script>
     document.addEventListener('DOMContentLoaded', function() {
  const componentContainer = document.querySelector('[tetra-component="main__default__address_form_component"]');

  function attachFormListener() {
    const form = document.getElementById('AddressForm');
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      const formData = new FormData(form);

      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value,
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.text())
      .then(html => updateComponent(html))
      .catch(error => console.error('Error:', error));
    });
  }

  function updateComponent(html) {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    const newComponentContainer = tempDiv.querySelector('[tetra-component="main__default__address_form_component"]');
    
    if (newComponentContainer) {
      componentContainer.innerHTML = newComponentContainer.innerHTML;
      Alpine.initTree(componentContainer);
      attachFormListener();
    } else {
      console.error('New component container not found in the response');
    }
  }

  attachFormListener();
});
</script>
    """
