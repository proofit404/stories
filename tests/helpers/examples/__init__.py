# flake8: noqa
import examples.context
import examples.context_contract_raw
import examples.contract
import examples.failure_reasons
import examples.methods
import examples.shortcuts


contract_modules = [examples.context_contract_raw]


try:
    import examples.context_contract_pydantic

    contract_modules.append(examples.context_contract_pydantic)
except (SyntaxError, ImportError):
    pass

try:
    import examples.context_contract_marshmallow

    contract_modules.append(examples.context_contract_marshmallow)
except ImportError:
    pass

try:
    import examples.context_contract_cerberus

    contract_modules.append(examples.context_contract_cerberus)
except ImportError:
    pass
