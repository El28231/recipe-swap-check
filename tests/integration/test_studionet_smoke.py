from pathlib import Path
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

ARGS = ["Whisk two eggs with milk, fold in wheat flour, and cook small pancakes on a lightly oiled pan.", "Replace the eggs while keeping enough binding for pancakes that can be flipped cleanly.", "The diner avoids eggs but has no listed soy allergy; use only the supplied culinary constraints."]

@pytest.mark.integration
def test_studionet_substitution_assessment(default_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "recipe_swap_check.py")
    deployed = factory.deploy_contract_tx(args=ARGS, account=default_account, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=default_account)
    proposed = contract.propose_substitution(args=["ground flax mixed with water", "The gel is proposed as a binder in place of the two eggs."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(proposed)
    assessed = contract.assess_proposal(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(assessed)
    proposal = contract.get_proposal(args=[1]).call()
    assert proposal["safety"] in ("SAFE", "UNSAFE", "UNCERTAIN")
    assert proposal["goal_fit"] in ("FIT", "PARTIAL", "NO_FIT")
    print(f"STUDIONET_ADDRESS={address}")
    print(f"STUDIONET_DEPLOY_TX={deployed['hash']}")
    print(f"STUDIONET_WRITE_TX={assessed['hash']}")
    print(f"STUDIONET_RESULT={proposal['safety']}/{proposal['goal_fit']}")

