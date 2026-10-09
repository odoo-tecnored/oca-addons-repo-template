from pathlib import Path

import pytest
import yaml
from copier import run_copy
from plumbum import local
from plumbum.cmd import git, pre_commit

PROJECT_ROOT = Path(__file__).parent.parent
COPIER_SETTINGS = yaml.safe_load((PROJECT_ROOT / "copier.yml").read_text())
LAST_ODOO_VERSION = max(COPIER_SETTINGS["odoo_version"]["choices"])


def _render(destination: Path, template: Path, odoo_version: float) -> None:
    """Render the template in ``destination`` with the standard test data."""
    data = {
        "odoo_version": odoo_version,
        "repo_slug": "website",
        "repo_name": "Test repo",
        "repo_description": "Test repo description",
    }
    run_copy(str(template), destination, data=data, defaults=True)


def test_hooks_installable(tmp_path: Path, odoo_version: float, cloned_template: Path):
    """Test that pre-commit hooks are installable."""
    _render(tmp_path, cloned_template, odoo_version)
    with local.cwd(tmp_path):
        git("init")
        pre_commit("install-hooks")


def test_render_passes_pre_commit(
    tmp_path: Path, odoo_version: float, cloned_template: Path
):
    """Test that the rendered repo passes every hook it ships.

    Hooks that rewrite files (prettier, ruff, oca-checks-odoo-module,
    oca-gen-external-dependencies, whool-init...) fail the CI when they have
    something to fix, so a rendered repo must already be clean. Only the newest
    Odoo version is checked: the point is to catch drift in the template
    sources, not to test every version combination.
    """
    if odoo_version != LAST_ODOO_VERSION:
        pytest.skip("pre-commit is only checked for the newest Odoo version")
    _render(tmp_path, cloned_template, odoo_version)
    with local.cwd(tmp_path):
        git("init")
        # `pre-commit run --all-files` only sees files known to git.
        git("add", "-A")
        # Same hook the rendered repo's own CI workflow skips.
        with local.env(SKIP="oca-gen-addon-readme"):
            pre_commit("run", "--all-files", "--show-diff-on-failure")
