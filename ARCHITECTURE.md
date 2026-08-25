# Architecture

## Responsibility boundary

The application may collect inputs and display state. RecipeSwapCheck owns the bounded on-chain record, authorization rules, semantic consensus call, and consequential state transition. There is no hidden backend or autonomous source collector.

## State machine

Open proposals -> per-proposal PENDING to assessed -> one owner-selected proposal.

## Storage model

The contract stores owner, recipe, goal, constraints, proposal texts/rationales/authors, safety and fit results, and selected number. Text is normalized and field-length-bounded before storage.

## Consensus boundary

The leader serializes only stored case data into canonical JSON and requests an exact JSON schema. Validators independently run the same prompt and normalization path. A validator accepts only an allowed, structurally valid value that exactly matches its own result. Exceptions and malformed output fail closed.

## Authorization and invariants

Anyone may propose before selection or assess a pending proposal. Only the owner can make the final eligible selection.

## Reuse and distinctness

Deploy one instance per recipe and substitution goal. The instance supports competing proposals and a final owner selection.

This is a many-proposal assess-then-select market, not a one-shot recipe classifier or pairwise proposal-conflict detector.
