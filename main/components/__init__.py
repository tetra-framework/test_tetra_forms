from main.models import Person, Book
from tetra import Library, public
from tetra.components import FormComponent

from main.forms import PersonForm, BookForm

default = Library()


@default.register
class PersonFormComponent(FormComponent):
    form_class = PersonForm

    def load(self, *args, **kwargs) -> None:
        self.persons = Person.objects.all()
        self.message: str = ""

    @public
    def remove(self,id: int) -> None:
        person = Person.objects.get(id=id)
        person.delete()
        self.message = f"Person {person} successfully deleted."

    # language=html
    template = """
    <div class='card'>
        <h3 class='card-title'>Create a new Person:</h3>
        {% csrf_token %}
        {{ form }}
        <button type='submit' @click='submit()'>Submit</button>    
        <p>Alpine.js: first_name: <span x-text='first_name'></span> 
        last_name: <span x-text='last_name'></span></p>
        <p>Django: first_name: {{first_name}} last_name: 
        {{last_name}}</p>
        <h4>Persons:</h4>
        <ul>
        {% for person in persons %}
          <li>
          {{person}}
          <button class="btn btn-danger btn-sm" 
                @click='remove({{person.id}})'>X</button>
          </li>
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

    @public
    def remove(self, id: int) -> None:
        book = Book.objects.get(id=id)
        book.delete()
        self.message = f"Book {book} successfully deleted."

    # language=html
    template = """
    <div class='card'>
        <h3 class='card-title'>Create a new Book:</h3>
        <h4>Testing ForeignKeys with Tetra</h4>
        {% csrf_token %}
        {{ form }}
        <button type='submit' @click='submit()'>Submit</button>    
        <p>Alpine.js: <span x-text='name'></span> 
        ( <span x-text='author'></span>, <span x-text='color'></span>)
        </p>
        <p>Django: {{name}} ({{author}}, {{color}})</p>
        <h4>Books:</h4>
        <ul>
        {% for book in books %}
          <li>
            {{book}}
            <button class="btn btn-danger btn-sm" 
                @click='remove({{book.id}})'>X</button>
          </li>
        {% endfor %}
        </ul>
        {{message}}
    </div>
    """
