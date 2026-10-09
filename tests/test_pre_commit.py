from pathlib import Path

import pytest
import yaml
from copier import run_copy
from plumbum import local
from plumbum.cmd import git, pre_commit

PROJECT_ROOT = Path(__file__).parent.parent
COPIER_SETTINGS = yaml.safe_load((PROJECT_ROOT / "copier.yml").read_text())
LAST_ODOO_VERSION = max(COPIER_SETTINGS["odoo_version"]["choices"])

# Hooks that rewrite files when the rendered repo is not already formatted.
# If the render does not pass them, every new repo needs a first
# `pre-commit run -a` commit before its CI can go green.
FORMATTING_HOOKS = ("prettier", "ruff-check", "ruff-format")


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


def test_render_passes_formatting_hooks(
    tmp_path: Path, odoo_version: float, cloned_template: Path
):
    """Test that the rendered repo already passes the formatting hooks it ships.

    Only the newest Odoo version is checked: the point is to catch formatting
    drift in the template sources, not to test every version combination.
    """
    if odoo_version != LAST_ODOO_VERSION:
        pytest.skip("formatting is only checked for the newest Odoo version")
    _render(tmp_path, cloned_template, odoo_version)
    with local.cwd(tmp_path):
        git("init")
        # `pre-commit run --all-files` only sees files known to git.
        git("add", "-A")
        pre_commit(
            "run",
            "--all-files",
            "--show-diff-on-failure",
            *FORMATTING_HOOKS,
        )
