import random

import toml
from chance import chance
from pytest_copie.plugin import Copie

LICENSE_SPEC = {
    'Apache-2.0': {'filename': 'LICENSE', 'stub': 'Apache License', 'with_holder': False},
    'BSD-3-Clause': {'filename': 'LICENSE', 'stub': 'BSD 3-Clause License', 'with_holder': True},
    'GPL-3.0-or-later': {'filename': 'COPYING', 'stub': 'GNU General Public License', 'with_holder': False},
    'LGPL-3.0-or-later': {'filename': 'COPYING', 'stub': 'GNU Lesser General Public License', 'with_holder': False},
    'MIT': {'filename': 'LICENSE', 'stub': 'MIT License', 'with_holder': True},
    'MPL-2.0': {'filename': 'LICENSE', 'stub': 'Mozilla Public License', 'with_holder': False},
    'Unlicense': {'filename': 'UNLICENSE', 'stub': 'This is free and unencumbered software released into the public domain', 'with_holder': False}
}


def generate_copier_answers():
    return {
        'project_name': f'{chance.word()}-{chance.word()}',
        'project_package': f'{chance.word()}_{chance.word()}',
        'project_description': chance.sentence(),
        'project_version': f'{random.randint(0, 10)}.{random.randint(0, 10)}.{random.randint(0, 10)}',
        'project_keywords': f'{chance.word()},{chance.word()},{chance.word()}',
        'copyright_holder_name': chance.name(),
        'copyright_holder_email': chance.email(),
        'copyright_license': chance.pickone(list(LICENSE_SPEC.keys())),
        'copyright_year': str(random.randint(2000, 2024)),
        'vcs_github_path': f'{chance.word()}/{chance.word()}-{chance.word()}'.lower(),
        'python_version': chance.pickone(['>=3.10', '>=3.11', '>=3.12']),
        'with_cli': False,
    }


def get_license_file(license_id: str) -> str:
    match license_id:
        case 'GPL-3.0-or-later' | 'LGPL-3.0-or-later':
            return 'COPYING'
        case 'Unlicense':
            return 'UNLICENSE'
        case _:
            return 'LICENSE'


def test_template_static_files(copie: Copie):
    result = copie.copy(extra_answers=generate_copier_answers())

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir.is_dir()

    assert result.project_dir.joinpath('.editorconfig').exists()
    assert result.project_dir.joinpath('CHANGELOG.md').exists()


def test_template_licenses(copie: Copie):
    for license_id, license_spec in LICENSE_SPEC.items():
        answers = generate_copier_answers()
        answers['copyright_license'] = license_id

        result = copie.copy(extra_answers=answers)

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_dir.is_dir()

        license_text = result.project_dir.joinpath(license_spec['filename']).read_text(encoding='utf-8')
        assert license_spec['stub'] in license_text

        if license_spec['with_holder']:
            assert f'{answers["copyright_holder_name"]} <{answers["copyright_holder_email"]}>' in license_text
            assert answers['copyright_year'] in license_text

        assert result.project_dir.joinpath(get_license_file(license_id)).exists()

        readme = result.project_dir.joinpath('README.md').read_text()

        assert answers['project_name'] in readme
        assert answers['project_description'] in readme

        assert license_spec['stub'] in readme

        if license_id == 'Unlicense':
            assert 'This is free and unencumbered software released into the public domain' in readme
        else:
            assert f'Copyright (C) {answers["copyright_year"]} {answers["copyright_holder_name"]} <{answers["copyright_holder_email"]}>' in readme
            assert f'see [{license_spec["filename"]}](./{license_spec["filename"]}).' in readme


def test_template_pyproject_toml(copie: Copie):
    answers = generate_copier_answers()
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir.is_dir()
    assert result.project_dir.joinpath('pyproject.toml').exists()

    with open(result.project_dir.joinpath('pyproject.toml'), 'r', encoding='utf-8') as fp:
        pyproject = toml.loads(fp.read())

    assert pyproject['project']['name'] == answers['project_name']
    assert pyproject['project']['version'] == answers['project_version']
    assert pyproject['project']['description'] == answers['project_description']
    assert pyproject['project']['requires-python'] == answers['python_version']
    assert pyproject['project']['authors'][0]['name'] == answers['copyright_holder_name']
    assert pyproject['project']['authors'][0]['email'] == answers['copyright_holder_email']
    assert pyproject['project']['license']['text'] == answers['copyright_license']
    assert pyproject['project']['keywords'] == answers['project_keywords'].split(',')

    assert pyproject['project']['urls']['homepage'] == f"https://github.com/{answers['vcs_github_path']}"
    assert pyproject['project']['urls']['repository'] == f"https://github.com/{answers['vcs_github_path']}.git"
    assert pyproject['project']['urls']['changelog'] == f"https://github.com/{answers['vcs_github_path']}/blob/main/CHANGELOG.md"


def test_template_package(copie: Copie):
    answers = generate_copier_answers()
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir.is_dir()

    init_file = result.project_dir / 'src' / answers['project_package'] / '__init__.py'
    assert init_file.exists()
    assert answers['project_package'] in init_file.read_text(encoding='utf-8')


def test_template_with_cli(copie: Copie):
    def with_cli_test(with_cli: bool):
        answers = generate_copier_answers()
        answers['with_cli'] = with_cli
        result = copie.copy(extra_answers=answers)

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_dir.is_dir()

        with open(result.project_dir.joinpath('pyproject.toml'), 'r', encoding='utf-8') as fp:
            pyproject = toml.loads(fp.read())

        assert ('click (>=8.1.8,<9.0.0)' in pyproject['project']['dependencies']) == with_cli

        if with_cli:
            cli = (result.project_dir / 'src' / answers['project_package'] / '__main__.py').read_text(encoding='utf-8')

            assert answers['project_package'] in cli
            assert answers['project_description'] in cli

            assert (result.project_dir / 'tests' / 'test_cli.py').exists()

        assert ('click' in (result.project_dir / 'tests' / 'conftest.py').read_text(encoding='utf-8')) == with_cli
        assert not (result.project_dir / 'tests' / 'test_example.py').exists() == with_cli

    with_cli_test(True)
    with_cli_test(False)
