# HySDS Pele Packaging Migration Summary

## Migration Completed: March 24, 2026

This document summarizes the migration of the `pele` repository from legacy `setup.py` to modern `pyproject.toml` packaging.

---

## Changes Made

### ✅ Files Created

1. **`pyproject.toml`** - Modern packaging configuration
   - Package name: `hysds-pele` (PyPI) / `pele` (import)
   - Version: Dynamic from git tags via `hatch-vcs`
   - Dependencies: 40+ third-party packages + 2 HySDS siblings
   - Moved test dependencies: `coverage`, `nodeenv` to dev extra

2. **`.github/workflows/publish.yml`** - PyPI publishing automation
   - Triggered on git tags (`v*`)
   - Uses PyPI Trusted Publishers (OIDC)

### ✅ Files Modified

1. **`pele/__init__.py`**
   - Added `__version__ = version("hysds-pele")` at the top

2. **`setup.py`**
   - Replaced with minimal shim for backward compatibility
   - Delegates all configuration to `pyproject.toml`
   - Will be removed in v7.1.0+

---

## Key Dependency Changes

### Fixed Issues

| Issue | Before | After |
|-------|--------|-------|
| Missing hysds-core | Not declared | `hysds-core~=7.0` |
| Missing hysds-commons | Not declared | `hysds-commons~=7.0` |
| coverage in main deps | `coverage` | Moved to dev extra |
| nodeenv in main deps | `nodeenv` | Moved to dev extra |

### Dependencies Preserved Exactly

All 40+ core dependencies maintained with exact pins from original `setup.py`, including:
- `Flask<2.3.0`
- `flask-restx>=0.5.1`
- Multiple Flask extensions
- `elasticsearch>=7.0.0,<7.14.0`
- `elasticsearch-dsl>=7.0.0,<7.4.0`
- `opensearch-py>=2.3.0,<3.0.0`
- `PyJWT==1.7.1`
- `bcrypt==3.2.2`
- `werkzeug<3.0.0`
- And many more...

---

## Build Verification

```bash
$ python -m build
Successfully built hysds_pele-1.4.0.post1.dev0+g... .tar.gz
Successfully built hysds_pele-1.4.0.post1.dev0+g... -py3-none-any.whl
```

---

## Next Steps

### Before Publishing to PyPI

1. **Verify sibling packages published first**
   - ✅ `hysds-core~=7.0` must be on PyPI
   - ✅ `hysds-commons~=7.0` must be on PyPI

2. **Tag version 7.0.0**
   ```bash
   git tag -a v7.0.0 -m "Release 7.0.0 - Modern packaging migration"
   git push origin v7.0.0
   ```

3. **Configure PyPI Trusted Publisher**
   - Go to https://pypi.org/manage/account/publishing/
   - Add GitHub Actions publisher for `hysds/pele` repo
   - Workflow: `publish.yml`
   - Environment: `pypi`

### Installation Methods

#### Development (Local)
```bash
pip install -e .
pip install -e ".[dev]"  # With dev dependencies
```

#### Development (From Git Branch)
```bash
pip install "git+https://github.com/hysds/pele.git@feature-branch"
```

#### Production (After PyPI Publishing)
```bash
pip install hysds-pele
```

---

## Backward Compatibility

### Import Names (Unchanged)
```python
# All existing imports continue to work
import pele
from pele import create_app
```

### Package Name Change
- **PyPI package**: `pele` → `hysds-pele`
- **Import name**: `pele` (unchanged)

---

## Migration Checklist

- [x] Create `pyproject.toml` with all dependencies
- [x] Add missing HySDS sibling dependencies
- [x] Move coverage and nodeenv to dev extra
- [x] Preserve all other dependency pins exactly
- [x] Update `pele/__init__.py` for dynamic versioning
- [x] Add GitHub Actions workflow for PyPI publishing
- [x] Keep minimal `setup.py` shim for backward compatibility
- [x] Verify `python -m build` succeeds
- [ ] Tag v7.0.0 release
- [ ] Configure PyPI Trusted Publisher
- [ ] Publish to PyPI

---

## Contact

For questions about this migration, contact the HySDS team at hysds-help@jpl.nasa.gov
