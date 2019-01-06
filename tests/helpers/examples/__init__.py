# flake8: noqa
import examples.context_contract_cerberus
import examples.context_contract_marshmallow
import examples.context_contract_raw
import examples.contract
import examples.failure_reasons
import examples.methods
import examples.shortcuts


contract_modules = [
    examples.context_contract_marshmallow,
    examples.context_contract_cerberus,
    examples.context_contract_raw,
]


try:
    import examples.context_contract_pydantic

    contract_modules.insert(0, examples.context_contract_pydantic)
except SyntaxError:
    pass
