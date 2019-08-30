from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    overload,
)

from cerberus.validator import Validator
from marshmallow.schema import Schema
from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import Field
from pydantic.main import BaseModel

from stories._context import Context
from stories._failures import NotNullExecProtocol, NullExecProtocol
from stories._marker import BeginningOfStory, EndOfStory
from stories._return import Failure, Result, Skip, Success


class PydanticValidator:
    def __init__(self, spec: BaseModel, field: Field) -> None: ...

    def __call__(self, value: Any) -> Any: ...

    def __repr__(self) -> str: ...


class MarshmallowValidator:
    def __init__(self, spec: Schema, field: str) -> None: ...

    def __call__(self, value: Any) -> Any: ...

    def __repr__(self) -> str: ...


class CerberusValidator:
    def __init__(self, spec: Validator, field: str) -> None: ...

    def __call__(self, value: Any) -> Any: ...

    def __repr__(self) -> str: ...


class RawValidator:
    def __init__(self, validator: Callable) -> None: ...

    def __call__(self, value: Any) -> Any: ...

    def __repr__(self) -> str: ...


def disassemble_pydantic(spec: BaseModel) -> Dict[str, PydanticValidator]: ...


def disassemble_marshmallow(spec: Schema) -> Dict[str, MarshmallowValidator]: ...


def disassemble_cerberus(spec: Validator) -> Dict[str, CerberusValidator]: ...


def disassemble_raw(spec: Dict[str, Callable]) -> Dict[str, RawValidator]: ...


@overload
def make_contract(
    cls_name: str, name: str, arguments: List[str], spec: None
) -> NullContract: ...


@overload
def make_contract(
    cls_name: str, name: str, arguments: List[str], spec: BaseModel
) -> SpecContract: ...


@overload
def make_contract(
    cls_name: str, name: str, arguments: List[str], spec: Schema
) -> SpecContract: ...


@overload
def make_contract(
    cls_name: str, name: str, arguments: List[str], spec: Dict[str, Callable]
) -> SpecContract: ...


def check_arguments_definitions(
    cls_name: str,
    name: str,
    arguments: List[str],
    spec: Dict[
        str,
        Union[MarshmallowValidator, PydanticValidator, RawValidator, CerberusValidator],
    ],
) -> None: ...


class NullContract:
    def __init__(self, cls_name: str, name: str, arguments: List[str]) -> None: ...

    def set_null(self) -> None: ...

    def make_argset(self) -> None: ...

    def check_story_call(self, kwargs: Dict[str, Any]) -> Dict[str, Any]: ...

    def check_substory_call(self, ctx: Context) -> None: ...

    def check_success_statement(
        self, method: Callable, ctx: Context, ns: Dict[str, Any]
    ) -> Dict[str, Any]: ...

    def __repr__(self) -> str: ...

    def format_contract_fields(self, *fieldset) -> str: ...


class SpecContract(NullContract):  # FIXME: Generic.
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

    def set_null(self) -> None: ...

    def make_argset(self) -> None: ...

    def make_declared(self) -> None: ...

    def check_story_call(
        self, kwargs: Dict[str, Union[Dict[str, str], str, int, List[int], List[str]]]
    ) -> Dict[str, Union[int, List[int], Dict[str, str], Dict[str, int]]]: ...

    def check_success_statement(
        self,
        method: Callable[[Context], Union[Result, Success, Failure, Skip]],
        ctx: Context,
        ns: Dict[str, Any],
    ) -> Dict[str, Any]: ...

    def identify(self, ns: Dict[str, Any]) -> Set[str]: ...

    def validate(self, ns: Dict[str, Any]) -> Any: ...

    def validate_spec(
        self,
        result: Dict[str, Union[Dict[str, str], int]],
        errors: Dict[str, Union[List[str], ErrorWrapper, str]],
        seen: Union[List[Tuple[str, str]], List[Tuple[str, Dict[str, str]]]],
        key: str,
        value: Union[List[str], Dict[str, str], str],
    ) -> None: ...

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

    def __repr__(self) -> str: ...

    def format_contract_fields(self, *fieldset) -> str: ...


def format_violations(ns: Dict[str, Any], errors: Dict[str, Any]) -> str: ...


def combine_contract(
    parent: Union[SpecContract, NullContract], child: Union[SpecContract, NullContract]
) -> None: ...


def combine_argsets(
    parent: Union[SpecContract, NullContract], child: Union[SpecContract, NullContract]
) -> None: ...


def combine_declared(parent: SpecContract, child: SpecContract) -> None: ...


def format_contract(
    contract: Union[SpecContract, NullContract]
) -> Optional[Union[Type[BaseModel], Type[Schema], Type[dict], Type[Validator]]]: ...


def maybe_extend_downstream_argsets(
    methods: List[
        Tuple[
            Union[BeginningOfStory, Callable, EndOfStory],
            Union[NullContract, SpecContract],
            Union[NullExecProtocol, NotNullExecProtocol],
        ],
    ],
    root: Union[SpecContract, NullContract],
) -> None: ...
