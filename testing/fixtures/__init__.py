from typing import TypeAlias

from fixtures import asynchronous
from fixtures import synchronous


S: TypeAlias = synchronous.Interface | asynchronous.Interface
