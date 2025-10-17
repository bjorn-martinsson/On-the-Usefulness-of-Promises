There are 4 hardness conditions of fiPCSP(A, OR), given by Theorem 5.16, 5.17, 5.18 and 5.21.

These hardness conditions are further based on 7 sub-conditions:

* `hardness_conditions/check_ADA_free.py`
* `hardness_conditions/check_ANDNOR_free.py`
* `hardness_conditions/check_bounded_inverted_matching.py`
* `hardness_conditions/check_bounded_matching.py`
* `hardness_conditions/check_unate.py`
* `hardness_conditions/check_UnCADA_free.py`
* `hardness_conditions/check_UnDADA_free.py`

The hardness conditions depend on the sub-conditions in the following way
```py
# All hardness conditions require ADA_free
if ADA_free(predicate):
    # Theorem 5.16
    if bounded_matching(predicate):
        return True

    # Theorem 5.17
    if bounded_inverted_matching(predicate):
        return True

    if unate(predicate):
        # Theorem 5.18
	if ANDNOR_free(predicate):
            return True

        # Theorem 5.21
        if UnCADA_free(predicate) and UnDADA_free(predicate):
            return True
return False
```

# Implementation details
The following 4 sub-conditions use a home made SAT-solver based only on unit propagation found in `hardness_conditions/unit_propagation.py`: ADA-free, UnCADA-free, UnDADA-free and bounded inverted matching. 

The following 2 sub-conditions generate all functions of low arity that would contradict sub-condition and check one by one that they all have obstructions: Bounded matching and unate.

The last sub-condition, to check if fiPCSP(predicate, OR) is ANDNOR-free, finds an obstruction matrix for ANDNOR, or proves none exists.

The reason why we use our own SAT-solver is that generating the entire SAT instance at once can be increadibly slow and use large amount of memory. By implementing our own SAT-solver we are able to mostly avoid this issue by avoiding to generate clauses that we already know to be satisfied.

The reason why we only use unit propagation instead a full SAT-solver is that it is simpler, faster, and from our testing ultimately does not seem to affect the result.

*Remark*: The checks for the sub-conditions may return false-negatives, i.e. it is possible that a sub-condition is actually satisfied without that being detected. This is either because we have limited our SAT-solver to unit-propagation or because we cannot use arbitrarily large arities. The exceptions to this are the ANDNOR-free checks and the unate checks. Both of these checks never result in a false-negative. 
