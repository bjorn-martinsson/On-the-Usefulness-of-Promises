This is a Python script (Python version >= 3.10) for verifying correctness of the tables found in ./tables, many of which appear in our paper.

It is highly recommended, but not required, to use PyPy instead of CPython for verification in the case of k = 5.
The reason is that CPython is significant slower than PyPy (which still takes hours to run).

To run the verification, simply run
`>>> python main.py`
or (if you have PyPy installed)
`>>> pypy3 main.py`

Dependencies:
* gurobipy, used in verification of tractability conditions.
* pysat, used in verification that unknowns are missing arbitrarily large block symmetries.

If a dependency is not found, then a warning will be displayed and that step will later be marked as *FAILED* in the summary of the verification.

*Remark*: This repo only contains a verification of our results. It does not contain the program we used to generate the tables in the first place.


# Summary of what is verified:

## Verification of tables corresponding to tractability and hardness of fiPCSP(A, OR)
* Coverage: Checks that the tables `maximal_tractable`, `minimal_hard`, `maximal_unknown` and `minimal_unknown` cover all possible predicates. It also verifies maximality/minimality. This uses bitsets of size 2^(2^k).
* Tractability: This checks that only the predicates found in the table `maximal_tractable` satisfies our tractability conditions.
* Hardness: This checks that only the predicates found in the table `minimal_hard` satisfies our hardness conditions.
* Block symmetries: This verifies that none of the predicates found in tables `maximal_unknown` and `minimal_unknown` have arbitrary large block-symmetric polymorphisms.
* Lexiographically smallest representatives: This checks that the predicates found in tables `maximal_tractable`, `minimal_hard`, `maximal_unknown` and `minimal_unknown` are the smallest possible with respect to permutations of the coordinates. This is not something that is important to our result, but it is something we claim is true.
* Counts: This checks that we get the same number of tractable/hard/unknown predicates as stated in our paper.

## Verification of tables correponding to promise-useful/uselessness
* Coverage: Checks that the tables `maximal_promise_useful`, `minimal_promise_useless`, `maximal_promise_unknown` and `minimal_promise_unknown` cover all possible predicates. It also verifies maximality/minimality. This uses bitsets of size 2^(2^k).
* Usefulness: This checks that only the predicates found in the table `maximal_promise_useful` are promise-useful based on the table `maximal_tractable`.
* Uselessness: This checks that only the predicates found in the table `minimal_promise_useless` are promise-useless based on the table `minimal_hard`.

* Lexiographically smallest representatives: This checks that the predicates found in tables `maximal_promise_useful`, `minimal_promise_useless`, `maximal_promise_unknown` and `minimal_promise_unknown` are the smallest possible with respect to permutations of the coordinates and xor with arbitrary bitstrings of length k. This is not something that is important to our result, but it is something we claim is true.
* Counts: This checks that we get the same number of promise-useful/useless/unknown predicates as stated in our paper.
