We consider 5 families of (block-)symmetric polymorphisms:

1. Majority
2. (odd) Parity
3. Alternating threshhold
4. Idempotized minority
5. Idempotized even parity

These can found in the following files.
* `check_majority.py`
* `check_parity.py`
* `check_AT.py`
* `check_idem_minority.py`
* `check_idem_even_parity.py`

Given a predicate A (a list of bit-strings of arity k), the `check`
function found in each file returns True if fiPCSP(A, OR) contains the corresponding family of (block-)symmetric polymorphisms. False otherwise.

The checks of majority, AT, and idempotized minorty make use of the LP-solver Gurobi. But the other two checks, of (odd) parity and idempotized even parity, are stand-alone.
