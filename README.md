# Test project for tetra forms

This is just a temporary testing project to test the functionality of tetra forms.
Don't bother bookmarking it. It will be deleted right after correct working form support and incorporated into `tetra.tests`.

## Installation

```bash
virtualenv .venv
. .venv/bin/activate
pip install tetra  # for testing the release version
# for testing a local tetra build you may have to install a development 
# version or a local branch instead
# pip install -e /path/to/local/tetra/install

# install this project too:
pip install -e .

# install node dependencies (esbuild for now)
npm install
```

Run

```bash
python manage.py migrate
python manage.py runserver
```
