# Development Notes

## Local build and install
The collection is built and installed into your local Ansible collections path.

```bash
source envrc
make install
```

The `make install` target:
- Builds the collection via `ansible-galaxy collection build`
- Installs the build artifact with `ansible-galaxy collection install`
- Removes the temporary tarball

This target requires `yq` to read the version from `merizrizal/idcloudhost/galaxy.yml`.

## Sanity lint test
```bash
make ansible-sanity-test-lint
```

This uses `ansible-doc` to discover the installed collection path and then runs:
```
ansible-test sanity --python-interpreter <python> --lint
```

## CI workflow
`.github/workflows/ansible-sanity-test-lint.yml` runs the lint sanity test on every push and pull request to `main` using Python 3.10, 3.11, and 3.12.
