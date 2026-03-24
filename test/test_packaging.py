"""Test packaging configuration and metadata."""
import sys
from importlib.metadata import version, requires

import pytest


def test_version_starts_with_7():
    """Verify package version starts with 7."""
    v = version("hysds-pele")
    assert v.startswith("7."), f"Expected version 7.x, got {v}"


def test_required_sibling_deps_declared():
    """Verify HySDS sibling dependencies are declared."""
    deps = requires("hysds-pele")
    assert deps is not None, "No dependencies found"
    
    dep_names = {dep.split()[0].split(";")[0].split(">=")[0].split("~=")[0].split("<")[0]
                 for dep in deps}
    
    required_siblings = {"hysds-core", "hysds-commons"}
    missing = required_siblings - dep_names
    
    assert not missing, f"Missing required HySDS deps: {missing}"


def test_coverage_nodeenv_in_dev_extra():
    """Verify coverage and nodeenv are in dev extra, not main dependencies."""
    deps = requires("hysds-pele")
    assert deps is not None
    
    main_dep_names = {dep.split()[0].split(";")[0].split(">=")[0].split("~=")[0].split("<")[0]
                      for dep in deps if "extra ==" not in dep}
    
    assert "coverage" not in main_dep_names, "coverage should be in dev extra, not main dependencies"
    assert "nodeenv" not in main_dep_names, "nodeenv should be in dev extra, not main dependencies"


def test_core_modules_importable():
    """Verify core pele modules can be imported."""
    import pele
    assert hasattr(pele, "__version__")


def test_python_version_requirement():
    """Verify running on Python 3.12+."""
    assert sys.version_info >= (3, 12), "Requires Python 3.12+"


def test_package_name_is_hysds_pele():
    """Verify package is published as hysds-pele."""
    v = version("hysds-pele")
    assert v is not None, "Package 'hysds-pele' not found"


def test_import_name_is_pele():
    """Verify import name remains 'pele' (not hysds_pele)."""
    import pele
    assert pele.__name__ == "pele"


def test_werkzeug_has_upper_bound():
    """Verify werkzeug has <3.0.0 upper bound."""
    deps = requires("hysds-pele")
    assert deps is not None
    
    werkzeug_deps = [d for d in deps if "werkzeug" in d.lower()]
    assert werkzeug_deps, "werkzeug dependency not found"
    
    for dep in werkzeug_deps:
        assert "<3.0" in dep or "<3" in dep, \
            f"werkzeug should have <3.0.0 upper bound, found: {dep}"
