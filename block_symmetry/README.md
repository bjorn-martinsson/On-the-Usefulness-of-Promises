`check_block_sym.py` contains a test for if fiPCSP(A, OR) does not contain arbitrarily large block-symmetric polymorphisms. 

The test is based on Theorem 2.12 in the paper, which states that fiPCSP(A, OR) has arbitrarily large block-symmetric polymorphisms iff fiPCSP(A, OR) contains an L x (L + 1) block symmetric function for all L >= 1.

`check_block_sym.py` uses a SAT-solver `Glucose3` found in `pysat.solvers` to tell whether or not there exists an L x (L + 1) block symmetric function for all L <= 11.

We use this test to show that any of our "unknown" predicates (for k = 5) do not contain arbitrarily large block-symmetric polymorphism,
and thus are not solvable by the BLP+AIP algorithm.
