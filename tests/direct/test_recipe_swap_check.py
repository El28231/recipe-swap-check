from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "recipe_swap_check.py"
SDK = "v0.2.16"
PROMPT = "independently assess a culinary ingredient"
ARGS = (
    "Whisk two eggs with milk, fold in wheat flour, and cook small pancakes on a lightly oiled pan.",
    "Replace the eggs while keeping enough binding for pancakes that can be flipped cleanly.",
    "Use only ordinary culinary information supplied here. The diner avoids eggs but has no listed soy allergy.",
)


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), *ARGS, sdk_version=SDK)


def test_many_proposals_assessed_then_owner_selects(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    contract.propose_substitution("ground flax mixed with water", "The gel is proposed as a binder in place of the two eggs.")
    direct_vm.mock_llm(PROMPT, json.dumps({"safety": "SAFE", "goal_fit": "FIT"}))
    contract.assess_proposal(1)
    direct_vm.sender = direct_alice
    contract.select_proposal(1)
    proposal = contract.get_proposal(1)
    assert proposal["selected"] is True
    assert proposal["author"] == "0x" + direct_bob.hex()
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_unsafe_proposal_cannot_be_selected(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    contract.propose_substitution("unidentified raw bean powder", "This unknown powder is proposed as a binder without preparation details.")
    direct_vm.mock_llm(PROMPT, json.dumps({"safety": "UNSAFE", "goal_fit": "PARTIAL"}))
    contract.assess_proposal(1)
    with direct_vm.expect_revert("proposal_not_selectable"):
        contract.select_proposal(1)


def test_invalid_assessment_fails_closed(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    contract.propose_substitution("mashed banana", "The mashed fruit is proposed to add moisture and some binding to the batter.")
    direct_vm.mock_llm(PROMPT, json.dumps({"safety": "SAFE", "goal_fit": "PERFECT"}))
    with direct_vm.expect_revert("invalid_assessment"):
        contract.assess_proposal(1)
    assert contract.get_proposal(1)["safety"] == "PENDING"

