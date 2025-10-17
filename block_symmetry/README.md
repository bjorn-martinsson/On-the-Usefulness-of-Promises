`check_block_sym.py` is able to tell if fiPCSP(A, OR) contains arbitrarily large block-symmetric polymorphisms. 

The test is based on Theorem 2.12, which states that fiPCSP(A, OR) has arbitrarily large block-symmetric polymorphisms iff fiPCSP(A, OR) contains an L x (L + 1) block symmetric function for all L >= 1.

`check_block_sym.py` uses a SAT-solver `Glucose3` found in `pysat.solvers` to test if there exists an L x (L + 1) block symmetric function for all L <= 11.

We use this test to show that any of our "unknown" predicates, k = 5, does not contain arbitrarily large block-symmetric polymorphism,
and thus are not solvable by the BLP+AIP algorithm.
