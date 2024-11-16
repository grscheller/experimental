# CHANGELOG

PyPI grscheller.experimental project.

#### Versioning schema

* first digits - always 0 to represent a perpetual pre-alpha state
* second digits - last PyPI release
* third digits - commit count since last PyPI release

## Releases and Important Milestones

### Version 

### Version 0.4.0 - PyPI release date 2024-10-20

* LAST PYPI RELEASE!!!
  * as a PyPI project grscheller.experimental will be OBSOLETED
  * the GitHub repo will continue
* migrated experimental.function to fp.functional
* `experimental.lazy` will be refactored for `fp.err_handling`
  * (f, arg1, arg2, arg3) is very well typed
  * may be base a lazy evaluation package around it
    * where argn: T|Lazy

### Version 0.3.0 - New experimental module added

* added experimental.functional
  * eventually slated to become the `fp.function` module
  * while lazy is tentatively slated to become `fp.lazy`
    * the `grscheller.lazy` PyPI project
* functional module developing tools for experimental.lazy
  * will need to learn and master ParamSpec

### Version 0.2.4 - Decided to go with 3 group versioning

* not a PyPI release
* middle digits change when an effort is added, removed, or moved
* previously moved Nada to `grscheller.fp.singletons`
* previously started non-strict function evaluation effort
  * `grscheller.experimental.lazy` module

### Version 0.1.1 - PyPI release date 2024-10-20

* removed docs from repo
* docs for all grscheller namespace projects maintained here
  * https://grscheller.github.io/grscheller-pypi-namespace-docs/

### Version 0.1.0 - PyPI Release: 2024-10-17

* Speculative new features for grscheller PyPI namespace projects
  * changing name grscheller.untyped to grscheller.experimental
  * decided to eventually make everything strictly typed
    * hence old name quite inappropriate
  * first PyPI release is a complete clone of grscheller.untyped
  * following PEP 423 - section "How to rename a project?"
  * project forever will be Pre-Alpha
