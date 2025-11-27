# dune-testpypi

## test tutorial action


This action has to be run manually to build the tutorial and update the
`doc` folder on the `main` branch of the
[github tutorial repositroy](https://github.com/dune-project/dune-fem-tutorial).

### Steps:

1. The `testing` workflow from the [testing repository](https://github.com/dune-project/dune-testpypi)
   is run to generate the packages with the next available version number. The
   tests are run by default if not deactivated in the input fields.
2. The tutorial scripts are executed. This is done for both `ubuntu` and
   `macOS` with an older and newer version of Python.
3. Together with the scripts the notebooks themselves are build and stored
   in artifact for the run with the newer Python on `ubuntu`.
4. The generated notebooks and the other content from the `doc` folder from
   the [dune-fempy](https://gitlab.dune-project.org/dune-fem/dune-fempy) repo is pushed
   to the `main` branch of
   [github tutorial repositroy](https://github.com/dune-project/dune-fem-tutorial)

### Input parameters:

- Download location: this can be either `dune`, `lund`, or `github`.
- Branches/tags: these can be provided for modules in the `core` and the
  `fem` namespace and separately for the `dune-fempy` repo itself.
- Testing: this activates or deactivates running the tests in the
  [testing repository](https://github.com/dune-project/dune-testpypi) repository.

# Sync/tag mirrors and upload action

This first syncs the github mirrors on `adedner` with the repos on the dune
gitlab server. This version is then tagged with the next available Python
package version available for the dune modules. After that the `test tutorial action` described above
is called with the source set to `github`, i.e, the just synced repos are
used to build the tutorial. On success the packages can be pushed to pypi and a new version
of the tutorial can be deployed.

### Steps:

1. First the github repos are synced and tagged. By default the tag used is
   determined automatically which means the next available version on `pypi` is used.
   But a tag can be prescribed.
2. The `test tutorial action` is called using the `github` repos as source
3. On failure the tag is removed again from the repos
   On success the repositories are uploaded to the destination requested
   and the `main` branch of the 
   [github tutorial repositroy](https://github.com/dune-project/dune-fem-tutorial)
   is pushed into another branch using the tag as name.

### Input parameters:


# Test ufl from source action

This is run every week in the night from Friday to Saturday testing the
tutorial using the developer version of ufl.
