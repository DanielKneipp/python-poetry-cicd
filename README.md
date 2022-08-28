# Python CICD example with `poetry` and GH actions

This project is a simple example on how to use GH actions and poetry to
implement Continuos Integration and Continuos Delivery for a python project
using `poetry` and `pytests`

The `master` branch is protect and can only be changed via PRs. Each PR has a `ci`
workflow with linting and tests. After a merge on `master`, another workflow
is responsible to build the package. There is also `Publish` step that should
push the package to a private repository following
[poetry docs](https://python-poetry.org/docs/master/libraries/#publishing-to-a-private-repository)

- [Python CICD example with `poetry` and GH actions](#python-cicd-example-with-poetry-and-gh-actions)
  - [CICD architecture](#cicd-architecture)
    - [Why just one job](#why-just-one-job)
  - [Local setup](#local-setup)
  - [Local operations](#local-operations)
    - [Test GH actions locally](#test-gh-actions-locally)
  - [Private repository configuration](#private-repository-configuration)
- [Resources](#resources)

## CICD architecture

The architecture follows a simple structure with two workflows:

1. The `ci` workflow with automation to run `pre-commit` for linting and dependency management checks.
Also test automation is included with test coverage report. This is executed on each PR to `master` and
must succeed to the PR to receive green light to be merged
2. The `cd` workflow, which has steps to build the python package and publish it to a private package repository
if the credentials are configured properly. This is executed after every merge on `master`. Since the tests
on every change have been executed already from the `ci` workflow, we can skip to the deployment actions

Both workflows reuse a `setup` action to configure the machine with the required dependencies. This setup
also caches the python virtualenv when nothing has changed in the `poetry.lock` file, making subsequent
workflow executions much faster.

### Why just one job

Each workflow has only one job with the same name. This is because every desired action must run sequentially and by using
just one job, we can continue to reuse the same runner reusing the setup step, reducing some execution time.

Separation of jobs make sense when you want to run things in parallel
([its default behavior]([snok/install-poetr](https://docs.github.com/en/actions/using-workflows/about-workflows#creating-dependent-jobs))).
A common case is to run tests with several [machine configurations](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs),
but since this is not the case of this project, one job is sufficient.

## Local setup

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="${HOME}/.local/bin:$PATH"

# Install dependencies
poetry shell
poetry install

# pre-commit setup
pre-commit install
```

> 💡 **Tip:** you can run `pre-commit run --all-files` to catch errors before committing

## Local operations

- **Lint**: `black *.py python_cicd/`
- **Test**: `pytest`
- **Build**: `poetry build`

Linting is already being done with `black` with `pre-commit` and is the recommended way to use it
locally or via GH workflows. The [gh-action](https://black.readthedocs.io/en/stable/integrations/github_actions.html)
from `black` docs could be used in the `ci` workflow, but `pre-commit` was used to streamline the process.

### Test GH actions locally

We can use [act](https://github.com/nektos/act) to test GH actions locally.

```bash
# Install act and GH cli
brew install act
brew install gh

# Authenticate with gh
gh auth login

# Test push-based workflows
act push --container-architecture linux/amd64

# Test pull_request-test workflows (there is a known issue with the `Comment coverage` step)
act pull_request --container-architecture linux/amd64 -s GITHUB_TOKEN=$(gh auth status -t 2>&1 | grep Token | awk '{print $3}')
```

> **Note**: There is a known issue with the `Comment coverage` step. It seems that act is
> not compatible with simulating interactions with PRs

## Private repository configuration

Poetry has documentation on how to [configure](https://python-poetry.org/docs/master/repositories/#publishing-to-a-private-repository)
and [publish](https://python-poetry.org/docs/master/libraries/#publishing-to-a-private-repository) on private repositories

This repo has a step on the `cd` workflow that tries to configure access and publish to a private repository like
[Sonatype Nexus](https://python-poetry.org/docs/master/libraries/#publishing-to-a-private-repository)
(assuming that a PyPI repository named `pypi-internal` has been create already). After configuring
the `REPO_USERNAME` and `REPO_PASSWORD` secrets in the repo, the `Publish` should execute on merges to `master`.

# Resources

- [workflow-builder](https://michaelcurrin.github.io/workflow-builder/#tips): Great tips for GH workflows design
- [Poetry docs](https://python-poetry.org/docs/master/)
- [Sonatype Nexus docs](https://help.sonatype.com/repomanager3/nexus-repository-administration/formats/pypi-repositories): As an example of PyPI repository
