from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "independently assess a culinary ingredient"
ARGS = ["Whisk two eggs with milk, fold in wheat flour, and cook small pancakes on a lightly oiled pan.", "Replace the eggs while keeping enough binding for pancakes that can be flipped cleanly.", "The diner avoids eggs but has no listed soy allergy; use only the supplied culinary constraints."]

def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"safety": "SAFE", "goal_fit": "FIT"})}})
    return {"validators": [v.to_dict() for v in validators]}

def test_five_validator_proposal_selection():
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "recipe_swap_check.py")
    deployed = factory.deploy_contract_tx(args=ARGS, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    contract = factory.build_contract(extract_contract_address(deployed))
    proposed = contract.propose_substitution(args=["ground flax mixed with water", "The gel is proposed as a binder in place of the two eggs."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(proposed)
    assessed = contract.assess_proposal(args=[1]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(assessed)
    selected = contract.select_proposal(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(selected)
    assert contract.get_state(args=[]).call()["selected_number"] == 1

