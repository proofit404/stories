from typing import Any, Callable, Dict, List, Union

from cerberus.validator import Validator

def contract_in(cls: Any, *args) -> Union[Callable, Dict[str, Callable], Validator]: ...
def failures_in(cls: Any, *args) -> Union[Callable, List[str]]: ...
