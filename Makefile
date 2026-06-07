UV ?= uv
MAKEFLAGS += --no-print-directory
export PYTHONUTF8 := 1

PACKAGE := ai_shell
PYTHON_TARGETS := ai_shell tests
PYLINT_MAIN_TARGETS := ai_shell
PYLINT_TEST_TARGETS := tests
MARKDOWN_TARGETS := README.md CHANGELOG.md docs/*.md
ABOUT_FILE := ai_shell/__about__.py
GHA_WORKFLOWS := .github/workflows

.PHONY: \
	help sync clean pre-commit-install \
	format format-python format-markdown \
	format-check format-check-python format-check-markdown \
	isort black \
	lint lint-check ruff-fix ruff-check pylint pylint-tests pylint-spelling bandit \
	spell \
	docs-check docs-check-docstrings docs-check-pydoctest check_docs build-docs make_docs \
	typecheck typecheck-mypy mypy \
	test test-ci smoke \
	metadata metadata-check version-check validate check_changelog \
	check_md check_spelling \
	security quality check check_all prerelease prerelease-check \
	gha-validate gha-pin gha-upgrade \
	publish-check publish publish_test \
	docker gen_code

help:
	@echo "Targets:"
	@echo "  sync                   Install / refresh dependencies"
	@echo "  format                 Auto-format Python and Markdown"
	@echo "  format-check           Check formatting without changes"
	@echo "  lint                   Ruff fix + pylint"
	@echo "  lint-check             Ruff check + pylint"
	@echo "  bandit                 Run security scan"
	@echo "  test                   Run pytest with coverage"
	@echo "  typecheck              Run mypy"
	@echo "  validate               Run release metadata and changelog validation"
	@echo "  check                  Main local quality gate"
	@echo "  prerelease             Full pre-release gate"

sync:
	@$(UV) sync

clean:
	@$(UV) run python -c "from pathlib import Path; import shutil; \
for path in ['build', 'dist', 'htmlcov', '.pytest_cache', '.ruff_cache', '.mypy_cache', '.coverage', 'junit.xml']; \
    p = Path(path); \
    shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink(missing_ok=True)"

pre-commit-install:
	@$(UV) run pre-commit install

# -- Formatting -----------------------------------------------------------------

format: format-python format-markdown

format-python:
	@$(UV) run isort $(PYTHON_TARGETS)
	@$(UV) run black $(PYTHON_TARGETS)
	@$(UV) run ruff check --fix --quiet $(PYTHON_TARGETS)
	@$(UV) run black $(PYTHON_TARGETS)

format-markdown:
	@$(UV) run mdformat $(MARKDOWN_TARGETS)

format-check: format-check-python format-check-markdown

format-check-python:
	@$(UV) run isort --check-only $(PYTHON_TARGETS)
	@$(UV) run black --check $(PYTHON_TARGETS)
	@$(UV) run ruff check --quiet $(PYTHON_TARGETS)

format-check-markdown:
	@$(UV) run mdformat --check $(MARKDOWN_TARGETS)

isort:
	@$(MAKE) format-python

black:
	@$(UV) run black $(PYTHON_TARGETS)

# -- Linting --------------------------------------------------------------------

lint: ruff-fix pylint pylint-tests

lint-check: ruff-check pylint pylint-tests

ruff-fix:
	@$(UV) run ruff check --fix --quiet $(PYTHON_TARGETS)

ruff-check:
	@$(UV) run ruff check --quiet $(PYTHON_TARGETS)

pylint:
	@$(UV) run pylint --score=n --reports=n --rcfile=.pylintrc $(PYLINT_MAIN_TARGETS)

pylint-tests:
	@$(UV) run pylint --score=n --reports=n --rcfile=.pylintrc_tests $(PYLINT_TEST_TARGETS)

pylint-spelling:
	@$(UV) run pylint --score=n --reports=n --rcfile=.pylintrc_spell $(PYLINT_MAIN_TARGETS)

bandit:
	@$(UV) run bandit -q -c pyproject.toml -r $(PACKAGE)

# -- Documentation / spelling ---------------------------------------------------

docs-check: docs-check-docstrings docs-check-pydoctest

docs-check-docstrings:
	@$(UV) run interrogate $(PACKAGE) --verbose

docs-check-pydoctest:
	@$(UV) run pydoctest --config .pydoctest.json | grep -v "__init__" | grep -v "__main__" | grep -v "Unable to parse" | grep -v "openai_toolkit"

check_docs: docs-check

build-docs:
	@$(UV) run pdoc -o docs_api $(PACKAGE)

make_docs: build-docs

spell: pylint-spelling
	@$(UV) run codespell --ignore-words=private_dictionary.txt $(PACKAGE) tests README.md CHANGELOG.md docs

check_spelling: spell

check_md:
	@$(UV) run mdformat --check $(MARKDOWN_TARGETS)

# -- Tests ----------------------------------------------------------------------

smoke:
	@$(UV) run ais --help
	@$(UV) run ais --version

test:
	@$(UV) run pytest -q --doctest-modules $(PACKAGE)
	@$(UV) run pytest -q tests --cov=$(PACKAGE) --cov-report=html --cov-fail-under 50

test-ci:
	@$(MAKE) test

# -- Type checking --------------------------------------------------------------

typecheck: typecheck-mypy

typecheck-mypy:
	@$(UV) run mypy --ignore-missing-imports --check-untyped-defs $(PACKAGE)

mypy: typecheck-mypy

# -- Release / metadata ---------------------------------------------------------

metadata:
	@$(UV) run metametameta pep621 --name $(PACKAGE) --source pyproject.toml --output $(ABOUT_FILE)

metadata-check:
	@$(UV) run metametameta sync-check --output $(ABOUT_FILE)

version-check:
	@$(UV) run jiggle_version check

check_changelog:
	@$(UV) run changelogmanager validate

validate: metadata-check version-check check_changelog

publish-check:
	@$(UV) build --no-sources
	@$(UV) run python -c "from pathlib import Path; [print(path.name) for path in sorted(Path('dist').glob('*'))]"

publish:
	@$(UV) publish

publish_test:
	@$(UV) publish --publish-url https://test.pypi.org/legacy/

# -- GitHub Actions maintenance -------------------------------------------------

gha-validate:
	@echo "Validating GitHub Actions workflows"
	@$(UV) run python -c "import pathlib, yaml; [yaml.safe_load(path.read_text(encoding='utf-8')) for path in pathlib.Path('$(GHA_WORKFLOWS)').glob('*.yml')]; print('YAML parse OK')"
	@$(UV) run python -c "\
from pathlib import Path; import yaml; \
data=yaml.safe_load(Path('$(GHA_WORKFLOWS)/release.yml').read_text(encoding='utf-8')); \
build_steps=data['jobs']['build']['steps']; \
publish_steps=data['jobs']['publish']['steps']; \
upload=next(step for step in build_steps if step.get('uses','').startswith('actions/upload-artifact@')); \
download=next(step for step in publish_steps if step.get('uses','').startswith('actions/download-artifact@')); \
assert upload['with']['name']==download['with']['name']=='packages'; \
assert upload['with']['path']==download['with']['path']=='dist/'; \
print('Artifact handoff OK:', upload['uses'], '->', download['uses'])"
	@$(UV) tool run --from zizmor zizmor --no-progress --no-exit-codes .

gha-pin:
	@echo "Pinning GitHub Actions to current SHAs"
	@$(UV) run python -c "import os, subprocess; token=os.environ.get('GITHUB_TOKEN'); \
result=None if token else subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=False); \
token=token or (result.stdout.strip() if result else ''); \
assert token, 'Set GITHUB_TOKEN or log in with gh auth login'; \
env=dict(os.environ, GITHUB_TOKEN=token); \
raise SystemExit(subprocess.run(['uv', 'tool', 'run', '--from', 'gha-update', 'gha-update'], env=env, check=False).returncode)"

gha-upgrade: gha-pin gha-validate
	@echo "GitHub Actions upgrade complete"

# -- Aggregate gates ------------------------------------------------------------

security: bandit

quality: format lint bandit test validate

check: lint-check security test typecheck validate
	@echo "All checks passed."

check_all: check check_docs check_md check_spelling

prerelease: check check_docs check_md check_spelling smoke publish-check
	@echo "Pre-release checks complete."

prerelease-check: prerelease

# -- Project-specific legacy targets -------------------------------------------

docker:
	docker build -t ai_shell -f Dockerfile .

gen_code:
	echo "Should check mypy and docstrings first."
	cd ai_shell && cd code_generate && python generate_schema.py
	cd ai_shell && cd code_generate && python generate_cli.py
	cd ai_shell && cd code_generate && python generate_toolkit.py
	pwd
