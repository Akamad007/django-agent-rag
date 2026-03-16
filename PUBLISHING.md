# Publishing

This repository publishes to PyPI with PyPI Trusted Publishing using GitHub Actions OIDC.
Only the `publish` job in `.github/workflows/python-publish.yml` receives `id-token: write`. The build job only needs read access.

## Release flow

1. Update the package version in `pyproject.toml`.
2. Push the change to GitHub.
3. Create a GitHub Release.
4. The workflow at `.github/workflows/python-publish.yml` builds the package and publishes it to PyPI.

You can also trigger the workflow manually with `workflow_dispatch`, but the trusted publisher configuration on PyPI must still match the same workflow file.

## PyPI Trusted Publishing configuration

On PyPI, configure a trusted publisher that matches:

- GitHub owner: `akamad007`
- Repository name: `django-agent-rag`
- Workflow filename: `.github/workflows/python-publish.yml`
- Environment name: `pypi`

The workflow path must match exactly. If PyPI is configured for a different workflow filename, publishing will fail.

## Important notes

- Do not use a PyPI API token for this workflow.
- Reusable GitHub workflows cannot currently be used as the trusted workflow for PyPI Trusted Publishing.
- Environment mismatches can cause publish failures even if the workflow itself is correct.
- Stale package names or PyPI URLs can also cause confusion. This package should be referenced as `django-agent-rag`, and the PyPI project URL should be `https://pypi.org/project/django-agent-rag/`.
- A trusted publisher configured for the wrong GitHub repository will fail even if the workflow file contents are correct.
