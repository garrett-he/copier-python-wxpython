import re
from packaging.specifiers import SpecifierSet
import subprocess
import sys
import unicodedata
from datetime import date

from jinja2.ext import Extension, Environment


def slugify_filter(value: str, separator: str = '-') -> str:
    value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-_\s]+', separator, value).strip('-_')


# pylint: disable=abstract-method
class DateExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.globals['current_year'] = date.today().year
        environment.globals['current_month'] = date.today().month
        environment.globals['current_day'] = date.today().day


# pylint: disable=abstract-method
class GitExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.globals['git_user_name'] = subprocess.getoutput('git config user.name').strip()
        environment.globals['git_user_email'] = subprocess.getoutput('git config user.email').strip()


# pylint: disable=abstract-method
class SlugifyExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.filters['slugify'] = slugify_filter


# pylint: disable=abstract-method
class ProjectExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.globals['dest_folder_name'] = sys.argv[4]


def version_list(value: str, versions: list[str]) -> list[str]:
    return list(SpecifierSet(value).filter(versions))


# pylint: disable=abstract-method
class VersionExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.filters['version_list'] = version_list
