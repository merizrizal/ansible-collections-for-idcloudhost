# Repository Structure

## Top-level
- `README.md` - Quickstart and collection overview
- `Makefile` - Build/install and lint sanity test target
- `envrc` - Local environment setup (sets `ROOT_DIR` and installs git hooks)
- `ci-envrc` - CI environment setup (sets `ROOT_DIR`)
- `.github/workflows/ansible-sanity-test-lint.yml` - GitHub Actions workflow
- `merizrizal/idcloudhost` - The Ansible collection root

## Collection root (`merizrizal/idcloudhost`)
- `README.md` - Collection summary
- `galaxy.yml` - Collection metadata
- `meta/runtime.yml` - Required Ansible version
- `plugins/` - Modules and module utilities

## Plugins
- `plugins/modules/` - Ansible modules
- `plugins/module_utils/` - Shared API helpers
