`check_block_sym.py` contains a check if fiPCSP(A, OR) contains arbitrarily large block-symmetric polymorphisms. 

The check is based on Theorem 2.12, which states that this is the case iff fiPCSP(A, OR) contains an L x (L + 1) block symmetric function for all L >= 1.

The check uses the SAT-solver `Glucose3` found in `pysat.solvers` to test if there exists an L x (L + 1) block symmetric function for all L <= 11.

We use `check_block_sym.py` to show that any predicate that is "unknown" predicate for k <= 5 does not contain arbitrarily large block-symmetric polymorphism,
and thus are not solved by the BLP+AIP algorithm.
