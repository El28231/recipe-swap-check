# Recipe Swap Check

Collects multiple ingredient-substitution proposals, evaluates each against supplied culinary constraints, and lets the recipe owner select an eligible option.

## Core workflow

- The owner stores the original recipe, culinary goal, and known constraints.
- Callers submit up to eight proposed swaps with rationales.
- Validators independently return safety and goal-fit categories for each proposal.
- The owner may select one proposal only when it is SAFE and FIT or PARTIAL.

## Reuse model

Deploy one instance per recipe and substitution goal. The instance supports competing proposals and a final owner selection.

## Why GenLayer

How a substitution affects binding, texture, technique, and stated constraints is a semantic culinary judgment. GenLayer supplies the shared assessment; deterministic code enforces selection eligibility.

## Evidence and source boundary

Only the stored recipe, goal, supplied constraints, proposed swap, and rationale are authoritative. The contract performs no nutrition, allergy, medical, or product-database lookup.

## Safety boundary

SAFE means only compatible with the supplied culinary constraints. It is not allergy, toxicology, nutritional, or medical certification. The contract holds no funds, has no upgrade hook, and never treats a model result as real-world certification.

## Verify locally

```text
python -m pip install -r requirements.txt
genvm-lint check contracts/recipe_swap_check.py
genvm-lint typecheck contracts/recipe_swap_check.py
pytest tests/direct -q
python tests/run_glsim.py --no-browser --seed 210821
gltest tests/integration/test_glsim_consensus.py -q --network localnet
```

Run the last two commands in separate terminals. Live StudioNet testing is opt-in and uses dedicated owner-specific keys outside this repository:

```text
gltest tests/integration/test_studionet_smoke.py -q -s --network studionet
```

Never commit a populated .env file, private key, keystore, or wallet password.

## Repository map

- contracts: deployable Intelligent Contract
- tests/direct: hardened state, authorization, malformed-output, and validator tests
- tests/integration: five-validator GLSim and live StudioNet flows
- deployments: public deployment and transaction evidence only
- SOURCE_POLICY.md: evidence authority and collection limits
- AUDIT.md: review-readiness checks and residual limitations
