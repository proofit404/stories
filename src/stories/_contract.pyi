from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

from cerberus.validator import Validator
from marshmallow.schema import Schema
from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import Field
from pydantic.main import BaseModel

from stories._context import Context
from stories._failures import NotNullExecProtocol, NullExecProtocol
from stories._marker import BeginningOfStory, EndOfStory

def check_arguments_definitions(
    cls_name: str,
    name: str,
    arguments: List[str],
    spec: Dict[
        str,
        Union[MarshmallowValidator, PydanticValidator, RawValidator, CerberusValidator],
    ],
) -> None: ...
def combine_argsets(
    parent: Union[SpecContract, NullContract], child: Union[SpecContract, NullContract]
) -> None: ...
def combine_contract(
    parent: Union[SpecContract, NullContract], child: Union[SpecContract, NullContract]
) -> None: ...
def combine_declared(parent: SpecContract, child: SpecContract) -> None: ...
def disassemble_cerberus(spec: Validator) -> Dict[str, CerberusValidator]: ...
def disassemble_marshmallow(spec: Any) -> Dict[str, MarshmallowValidator]: ...
def disassemble_pydantic(spec: Any) -> Dict[str, PydanticValidator]: ...
def disassemble_raw(spec: Dict[str, Callable]) -> Dict[str, RawValidator]: ...
def format_contract(
    contract: Union[SpecContract, NullContract]
) -> Optional[Union[Type[BaseModel], Type[Schema], Type[dict], Type[Validator]]]: ...
def format_violations(
    ns: Dict[str, Union[str, List[int], List[str]]], errors: Dict[str, Any]
) -> str: ...
def make_contract(
    cls_name: str, name: str, arguments: List[str], spec: Any
) -> Union[SpecContract, NullContract]: ...
def maybe_extend_downstream_argsets(
    methods: Union[
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                Tuple[Callable, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NullExecProtocol],
            ]
        ],
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NotNullExecProtocol],
                Tuple[Callable, NullContract, NotNullExecProtocol],
                Tuple[EndOfStory, NullContract, NotNullExecProtocol],
            ]
        ],
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NullExecProtocol],
            ]
        ],
        List[
            Union[
                Tuple[BeginningOfStory, SpecContract, NullExecProtocol],
                Tuple[Callable, SpecContract, NullExecProtocol],
                Tuple[EndOfStory, SpecContract, NullExecProtocol],
            ]
        ],
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NotNullExecProtocol],
                Tuple[Callable, NullContract, NotNullExecProtocol],
                Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                Tuple[Callable, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NotNullExecProtocol],
            ]
        ],
    ],
    root: Union[SpecContract, NullContract],
) -> None: ...

class CerberusValidator:
    def __call__(
        self, value: Union[List[int], str, Dict[str, str], List[str]]
    ) -> Any: ...
    def __init__(self, spec: Validator, field: str) -> None: ...
    def __repr__(self) -> str: ...

class MarshmallowValidator:
    def __call__(
        self, value: Union[List[int], str, Dict[str, str], List[str]]
    ) -> Any: ...
    def __init__(self, spec: Any, field: str) -> None: ...
    def __repr__(self) -> str: ...

class NullContract:
    def __init__(self, cls_name: str, name: str, arguments: List[str]) -> None: ...
    def __repr__(self) -> str: ...
    def check_story_call(self, kwargs: Dict[str, Any]) -> Dict[str, Any]: ...
    def check_substory_call(self, ctx: Context) -> None: ...
    def check_success_statement(
        self, method: Callable, ctx: Context, ns: Dict[str, Any]
    ) -> Dict[str, Any]: ...
    def format_contract_fields(self, *fieldset) -> str: ...
    def make_argset(self) -> None: ...
    def set_null(self) -> None: ...

class PydanticValidator:
    def __call__(
        self, value: Union[str, List[int], List[str], Dict[str, str]]
    ) -> Any: ...
    def __init__(self, spec: Any, field: Field) -> None: ...
    def __repr__(self) -> str: ...

class RawValidator:
    def __call__(
        self, value: Union[str, List[str], List[int], Dict[str, str]]
    ) -> Any: ...
    def __init__(self, validator: Callable) -> None: ...
    def __repr__(self) -> str: ...

class SpecContract:
    def __init__(
        self,
        cls_name: str,
        name: str,
        arguments: List[str],
        spec: Dict[
            str,
            Union[
                MarshmallowValidator, PydanticValidator, RawValidator, CerberusValidator
            ],
        ],
        origin: Any,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def assign_result(
        self,
        result: Dict[str, Union[Dict[str, str], str, int, List[int]]],
        seen: Union[
            List[Tuple[str, str]],
            List[Union[Tuple[str, str], Tuple[str, List[str]]]],
            List[Tuple[str, Dict[str, str]]],
        ],
        key: str,
        value: Union[List[int], str, Dict[str, str], List[str]],
        new_value: Any,
    ) -> None: ...
    def check_story_call(
        self, kwargs: Dict[str, Union[Dict[str, str], str, int, List[int], List[str]]]
    ) -> Dict[str, Union[int, List[int], Dict[str, str], Dict[str, int]]]: ...
    def check_success_statement(
        self,
        method: Callable,
        ctx: Context,
        ns: Dict[str, Union[str, List[str], Dict[str, str]]],
    ) -> Dict[str, Any]: ...
    def format_contract_fields(self, *fieldset) -> str: ...
    def identify(
        self, ns: Dict[str, Union[str, List[str], Dict[str, str]]]
    ) -> Set[str]: ...
    def make_argset(self) -> None: ...
    def make_declared(self) -> None: ...
    def set_null(self) -> None: ...
    def validate(
        self, ns: Dict[str, Union[Dict[str, str], str, List[int], List[str]]]
    ) -> Any: ...
    def validate_argset(
        self,
        result: Dict[str, Union[Dict[str, str], str, int, List[int]]],
        errors: Dict[str, Union[List[str], ErrorWrapper, str]],
        seen: Union[
            List[Tuple[str, str]],
            List[Union[Tuple[str, str], Tuple[str, List[str]]]],
            List[Tuple[str, Dict[str, str]]],
        ],
        conflict: Dict[Tuple[str, str], Dict[str, Union[int, str]]],
        key: str,
        value: Union[List[int], List[str], Dict[str, str], str],
    ) -> None: ...
    def validate_spec(
        self,
        result: Dict[str, Union[Dict[str, str], int]],
        errors: Dict[str, Union[List[str], ErrorWrapper, str]],
        seen: Union[List[Tuple[str, str]], List[Tuple[str, Dict[str, str]]]],
        key: str,
        value: Union[List[str], Dict[str, str], str],
    ) -> None: ...
