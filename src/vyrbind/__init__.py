"""VyrBind: deterministic, fail-closed local AI action boundary."""
from .models import ContractError, Intent, Result, RunContract
from .evidence import EvidenceLedger, IntegrityError
from .broker import LocalBroker
from .policy import Verdict, evaluate

__version__ = "0.1.0"
__all__ = ["Intent", "RunContract", "LocalBroker", "EvidenceLedger", "Result", "Verdict", "evaluate", "ContractError", "IntegrityError"]
