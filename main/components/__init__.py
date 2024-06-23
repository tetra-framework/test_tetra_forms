from main.models import Person, Book
from tetra import Library
from tetra.components import FormComponent

from main.forms import PersonForm, BookForm

default = Library()


@default.register
class PersonFormComponent(FormComponent):
    form_class = PersonForm

    def load(self, *args, **kwargs) -> None:
        self.persons = Person.objects.all()
        self.message: str = ""

    # language=html
    template = """
    <div class='card'>
        <h3 class='card-title'>Create a new Person:</h3>
        {% csrf_token %}
        {{ form }}
        <button type='submit' @click='submit()'>Submit</button>    
        <p>Frontent var, Alpine.js says: <span x-text='first_name'></span> <span x-text='last_name'></span></p>
        <p>Backend var, Django says: {{first_name}} {{last_name}}</p>
        <h4>Persons:</h4>
        <ul>
        {% for person in persons %}
          <li>{{person}}</li>
        {% endfor %}
        </ul>
        {{message}}
    </div>
    """

    def form_valid(self, form) -> None:
        Person.objects.create(first_name=self.first_name, last_name=self.last_name)
        self.message = "Person successfully saved."

    def form_invalid(self, form) -> None:
        self.message = "Error saving person."


@default.register
class BookFormComponent(FormComponent):
    form_class = BookForm

    def load(self, *args, **kwargs) -> None:
        self.books = Book.objects.all()
        self.message: str = ""

    def form_valid(self, form) -> None:
        Book.objects.create(first_name=self.name)
        self.message = "Book successfully saved."

    def form_invalid(self, form) -> None:
        self.message = "Error saving book."

    # language=html
    template = """
    <div class='card'>
        <h3 class='card-title'>Create a new Book:</h3>
        {% csrf_token %}
        {{ form }}
        <button type='submit' @click='submit()'>Submit</button>    
        <p>Frontent var, Alpine.js says: <span x-text='name'></p>
        <p>Backend var, Django says: {{name}}</p>
        <h4>Books:</h4>
        <ul>
        {% for book in books %}
          <li>{{book}}</li>
        {% endfor %}
        </ul>
        {{message}}
    </div>
    """
