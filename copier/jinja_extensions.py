# pylint: disable=abstract-method
import re
import subprocess
import unicodedata
from datetime import date

from jinja2.ext import Extension, Environment
from packaging.specifiers import SpecifierSet


def slugify_filter(value: str, separator: str = '-') -> str:
    value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-_\s]+', separator, value).strip('-_')


def version_list(value: str, versions: list[str]) -> list[str]:
    return list(SpecifierSet(value).filter(versions))


class DateExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.globals['current_year'] = date.today().year
        environment.globals['current_month'] = date.today().month
        environment.globals['current_day'] = date.today().day


class GitExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.globals['git_user_name'] = subprocess.getoutput('git config user.name').strip()
        environment.globals['git_user_email'] = subprocess.getoutput('git config user.email').strip()


class SlugifyExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.filters['slugify'] = slugify_filter


class VersionExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.filters['version_list'] = version_list
