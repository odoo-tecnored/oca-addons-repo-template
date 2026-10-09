# TD Logiciel Addons Repo Template

This is a template created to make easier the task of maintaining TD Logiciel addon
repositories.

## Why?

We have several repos. Most of them look the same, and most of them need
specific-but-similar configurations for CI, code quality, dependency management, etc.

We need a place where to evolve those things and push them automatically everywhere
else.

This is that place.

## How to use?

This is a template. It is based on [Copier](https://github.com/pykong/copier), go there
to read its docs to know how it works.

Quick answer to bootstrap a new repo:

```bash
# Install copier and pre-commit if missing
pipx install copier
pipx install pre-commit
pipx ensurepath
# Clone this template and answer its questions
copier copy https://github.com/odoo-tecnored/oca-addons-repo-template.git some-repo
# Commit that
cd some-repo
git add .
pre-commit install
pre-commit run -a
git commit -am 'Hello world 🖖'
```

Quick answer to update a repo:

```bash
# Update the repo
cd some-repo
copier update
# Reformat updated files
pre-commit run
# Commit update
git commit -am 'Updated from template'
# Reformat all other files, in case some pre-commit configuration was updated
pre-commit run -a || git commit -am 'Reformatted after template update'
```

## How to contribute?

Go read [our contribution guideline](CONTRIBUTING.md).

## Supported use cases

This template allows to bootstrap and update addon repositories for these Odoo versions:

- 11.0
- 12.0
- 13.0
- 14.0
- 15.0
- 16.0
- 17.0
- 18.0
- 19.0
- 20.0

Future versions will be added as they are released. Past versions could be added as long
as they don't break existing branches.

This template is based on the OCA addons repo template, adapted for TD Logiciel, C.A.
You might find some things that you can reuse in your own templates, but in general
terms this template is meant to be used by TD Logiciel, C.A.

## The legal stuff

Copyright holder: [TD Logiciel, C.A.](https://github.com/odoo-tecnored).

Template license: [MIT](LICENSE)

License of the rendered repositories: OPL-1 (proprietary, TD Logiciel, C.A.)

License of each module in those rendered repositories: Depends on the module.
