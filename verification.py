from bitset import bitset
import parse_tables
from block_symmetry.check_block_sym import check_block_sym
from functools import lru_cache as memoization

"""
    This file contains functions for verifying correctness of the tables corresponding
    to tractability and hardness of fiPCSP(A, OR).
"""

@memoization
def get_tables(k:int) -> tuple[list[list[str]]]:
    # Table with "hardest" tracable predicates
    maximal_tractable = parse_tables.read('tables/maximal_tractable_k%d.txt' % k)
    
    # Table  with "easiest" hard predicates
    minimal_hard = parse_tables.read('tables/minimal_hard_k%d.txt' % k)
    
    # Table with "hardest" unknown predicates
    maximal_unknown = parse_tables.read('tables/maximal_unknown_k%d.txt' % k)
    
    # Table with "easiest" unknown predicates
    minimal_unknown = parse_tables.read('tables/minimal_unknown_k%d.txt' % k)
    return maximal_tractable, minimal_hard, maximal_unknown, minimal_unknown

def apply_permutation(predicate: list[str], permutation: list[int]) -> list[str]:
    out = []
    for assign in predicate:
        permuted_assignment = ''.join(assign[i] for i in permutation)
        out.append(permuted_assignment)
    out.sort()
    return out

def all_permutations(predicate: list[str]) -> list[list[str]]:
    if not predicate:
        return []

    import itertools
    k = len(predicate[0])
    permutations = itertools.permutations(range(k))

    out = []
    for permutation in permutations:
        permuted_predicate = apply_permutation(predicate, permutation)
        if permuted_predicate not in out:
            out.append(permuted_predicate)

    return out

def predicate_to_bitmask(predicate: list[str]) -> int:
    out = 0
    for assign in predicate:
        out |= 1 << int(assign, 2)
    return out

@memoization
def get_bitsets(k: int) -> tuple[bitset]:
    maximal_tractable, minimal_hard, maximal_unknown, minimal_unknown = get_tables(k)
    m = 2**(2**k)
    
    # Find all tractable predicates
    tractable_bitset = bitset(m)
    
    # Fill in the maximal tractable predicates
    for predicate in maximal_tractable:
        for p in map(predicate_to_bitmask, all_permutations(predicate)):
            tractable_bitset[p] = 1
    
    # Fill in implications
    for i in range(0, m, 2)[::-1]:
        if tractable_bitset[i]:
            for bit in range(1, 2**k):
                i2 = i & ~(1 << bit)
                tractable_bitset[i2] = 1
    
    # Find all hard predicates
    hard_bitset = bitset(m)
    
    # Fill in the minimal hard predicates
    for predicate in minimal_hard:
        for p in map(predicate_to_bitmask, all_permutations(predicate)):
            hard_bitset[p] = 1
    
    # Fill in implications
    for i in range(0, m, 2):
        if hard_bitset[i]:
            for bit in range(1, 2**k):
                i2 = i | (1 << bit)
                hard_bitset[i2] = 1

    
    # Find all tractable + unknown predicates
    tractable_and_unknown_bitset = tractable_bitset.copy()
    
    # Fill in the maximal unknown predicates
    for predicate in maximal_unknown:
        for p in map(predicate_to_bitmask, all_permutations(predicate)):
            tractable_and_unknown_bitset[p] = 1
    
    # Fill in implications
    for i in range(0, m, 2)[::-1]:
        if tractable_and_unknown_bitset[i]:
            for bit in range(1, 2**k):
                i2 = i & ~(1 << bit)
                tractable_and_unknown_bitset[i2] = 1

    
    # Find all hard + unknown predicates
    hard_and_unknown_bitset = hard_bitset.copy()
    
    # Fill in the minimal unknown predicates
    for predicate in minimal_unknown:
        for p in map(predicate_to_bitmask, all_permutations(predicate)):
            hard_and_unknown_bitset[p] = 1
    
    # Fill in implications
    for i in range(0, m, 2):
        if hard_and_unknown_bitset[i]:
            for bit in range(1, 2**k):
                i2 = i | (1 << bit)
                hard_and_unknown_bitset[i2] = 1


    # Unknown predicates lie in the intersection of the two bitsets
    unknown_bitset = tractable_and_unknown_bitset & hard_and_unknown_bitset
    return tractable_bitset, unknown_bitset, hard_bitset

def verify_coverage(k: int) -> bool:
    """
        The minimal/maximal tables should cover all possible predicates.
        This verifies that all predicates are covered, and that the minimal/maximal
        tables are actually minimal/maximal.
    """
    maximal_tractable, minimal_hard, maximal_unknown, minimal_unknown = get_tables(k)
    tractable_bitset, unknown_bitset, hard_bitset = get_bitsets(k)
    m = 2**(2**k) # Size of the bitsets

    # Check that none of the 3 regions (tractable, unknown, hard) intersect
    assert (tractable_bitset & unknown_bitset).sum() == 0
    assert (tractable_bitset & hard_bitset).sum() == 0
    assert (unknown_bitset & hard_bitset).sum() == 0

    # Check that their union is everything
    
    assert (tractable_bitset).sum() + (unknown_bitset).sum() + (hard_bitset).sum() == m//2 

    # Verify maximality of maximal_tractable
    for predicate in maximal_tractable:
        # Check that any larger predicate is not tractable
        p = predicate_to_bitmask(predicate)
        assert tractable_bitset[p]
        for bit in range(1, 2**k):
            if p & (1 << bit) == 0:
                assert not tractable_bitset[p | (1 << bit)]

    # Verify minimality of minimal_hard
    for predicate in minimal_hard:
        # Check that any smaller predicate is not hard
        p = predicate_to_bitmask(predicate)
        assert hard_bitset[p]
        for bit in range(1, 2**k):
            if p & (1 << bit):
                assert not hard_bitset[p | ~(1 << bit)]

    # Verify maximality of maximal_unknown
    for predicate in maximal_unknown:
        # Check that any larger predicate is not unknown
        p = predicate_to_bitmask(predicate)
        assert unknown_bitset[p]
        for bit in range(1, 2**k):
            if p & (1 << bit) == 0:
                assert not unknown_bitset[p | (1 << bit)]
    
    # Verify minimality of minimal_unknown
    for predicate in minimal_unknown:
        # Check that any smaller predicate is not unknown
        p = predicate_to_bitmask(predicate)
        assert unknown_bitset[p]
        for bit in range(1, 2**k):
            if p & (1 << bit):
                assert not unknown_bitset[p | ~(1 << bit)]

    return True

def is_tractable(predicate: list[str]) -> bool:
    """
    Check if fiPCSP(predicate, OR) contains any of the (block)-symmetric families
    1. Majority
    2. (odd) Parity
    3. Alternating threshhold
    4. Idempotenized even party
    5. Idempotenized minority 
    """

    # Import the check-function from the python files used to test if majority/parity/etc... are polymorphism
    tractability_conditions = ["check_majority", "check_parity", "check_AT", "check_idem_even_parity", "check_idem_minority"]
    checks = [__import__("tractability_conditions." + condition, fromlist = [condition]).check for condition in tractability_conditions]
    
    # The predicate is tractable if it contains at least one block-symmetric family
    return any(check(predicate) for check in checks)

def verify_tractability(k: int) -> bool:
    """
    Verifies that: 
        1. At least one tractability condition is satisfied for every predicate in maximal_tractable
        2. No tractability conditions are satisfied for predicates in minimal_hard, minimal_unknown, maximal_unknown
    """
    maximal_tractable, minimal_hard, maximal_unknown, minimal_unknown = get_tables(k)

    try:
        import gurobipy as gp
    except ModuleNotFoundError:
        print('Warning: Module gurobipy not found. Verification of tractability conditions requires gurobipy.')
        print('Aborting.')
        return False

    for predicate in maximal_tractable:
        assert is_tractable(predicate)

    for predicate in minimal_hard + minimal_unknown + maximal_unknown:
        assert not is_tractable(predicate)

    return True

def is_hard(predicate: list[str]) -> bool:
    """
    Checks if predicate satisfies any of the hardness conditions given by Theorems
    5.16, 5.17, 5.18 or 5.21.

    Return True if satisfies at least one. Otherwise return False.

    Remark: Note that a predicate could in theory satisfy a hardness condition,
            but where our tests are unnable to confirm that such is the case.
            However, we cannot get a false positive.
    """
    import hardness_conditions.check_ADA_free
    import hardness_conditions.check_ANDNOR_free
    import hardness_conditions.check_bounded_inverted_matching
    import hardness_conditions.check_bounded_matching
    import hardness_conditions.check_unate
    import hardness_conditions.check_UnCADA_free
    import hardness_conditions.check_UnDADA_free

    ADA_free = hardness_conditions.check_ADA_free.check
    ANDNOR_free = hardness_conditions.check_ANDNOR_free.check
    bounded_inverted_matching = hardness_conditions.check_bounded_inverted_matching.check
    bounded_matching = hardness_conditions.check_bounded_matching.check
    unate = hardness_conditions.check_unate.check
    UnCADA_free = hardness_conditions.check_UnCADA_free.check
    UnDADA_free = hardness_conditions.check_UnDADA_free.check

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

def verify_hardness(k: int) -> bool:
    """
    Verifies that: 
        1. At least one hardness condition is satisfied for every predicate in maximal_hard
        2. No hardness conditions are satisfied for predicates in maximal_tractable, minimal_unknown, maximal_unknown
    """
    maximal_tractable, minimal_hard, maximal_unknown, minimal_unknown = get_tables(k)

    for predicate in minimal_hard:
        assert is_hard(predicate)
    
    for predicate in maximal_tractable + minimal_unknown + maximal_unknown:
        assert not is_hard(predicate)
    
    return True

def is_missing_block_sym(predicate: list[str]) -> bool:
    L, assign = check_block_sym(predicate)
    # Emtpy truth table corresponds to missing block symmetric polymorphism
    return len(assign) == 0

def verify_block_sym(k: int) -> bool:
    """
    Verifies that, for every predicate in minimal_hard, maximal_unknown and minimal_unknown, 
    there exists some L such that the predicate does not have an L x (L + 1) block symmetric polymorphism.
    """
    maximal_tractable, minimal_hard, maximal_unknown, minimal_unknown = get_tables(k)
    try:
        from pysat.solvers import Glucose3
    except ModuleNotFoundError:
        print('Warning: Module pysat not found. Pysat is required to disprove existence of block symmetric polymorphisms.')
        print('Aborting.')
        return False

    for predicate in minimal_hard + maximal_unknown + minimal_unknown:
        assert is_missing_block_sym(predicate)

    return True

def verify_representative_lexographically_smallest(k: int) -> bool:
    """
    Verifies that the representatives are lexographically smallest with respect to permutations.
    Additionally verifies that representatives in each table are given in lexiographical order.
    """
    maximal_tractable, minimal_hard, maximal_unknown, minimal_unknown = get_tables(k)
    for predicate in maximal_tractable + minimal_hard + maximal_unknown + minimal_unknown:
        p1 = predicate_to_bitmask(predicate)
        for predicate2 in all_permutations(predicate):
            p2 = predicate_to_bitmask(predicate2)
            assert p1 <= p2
    
    for predicates in maximal_tractable, minimal_hard, maximal_unknown, minimal_unknown:
        prev = None
        for predicate in predicates:
            p = predicate_to_bitmask(predicate)
            assert prev == None or prev < p
            prev = p

    return True

@memoization
def get_representatives(k: int) -> list[int]:
    """
    Computes all representatives with respect to permutations.
    """

    # Uses bitmasks instead of bitstrings for enhanced performance
    import itertools
    permutations = itertools.permutations(range(k)) 
    maps = []
    for permutation in permutations:
        mapping = [0] * 2**k
        for bitstring in parse_tables.all_bitstrings(k):
            permuted_bitstring = ''.join(bitstring[i] for i in permutation)
            mapping[int(bitstring, 2)] = int(permuted_bitstring, 2)
        maps.append(mapping)

    def apply_map(p, mapping):
        q = 0
        for i in range(2**k):
            q |= ((p >> i) & 1) << mapping[i]
        return q

    representatives = []
    m = 2**(2**k)
    found = bitset(m)
    for p in range(2, m, 2):
        if found[p]:
            continue
        representatives.append(p)
        for mapping in maps:
            q = apply_map(p, mapping)
            found[q] =1
    
    return representatives

def verify_counts(k: int) -> bool:
    """
    Checks that the counts of tractable/hard/unknown predicate matches the numbers in the paper
    """
    tractable_bitset, unknown_bitset, hard_bitset = get_bitsets(k)
    representatives = get_representatives(k)

    tractable_count = unknown_count = hard_count = 0
    for p in representatives:
        if tractable_bitset[p]:
            tractable_count += 1
        if unknown_bitset[p]:
            unknown_count += 1
        if hard_bitset[p]:
            hard_count += 1

    assert len(representatives) == tractable_count + unknown_count + hard_count

    if k == 2:
        assert tractable_count == 5
        assert unknown_count   == 0
        assert hard_count      == 0
    elif k == 3:
        assert tractable_count == 33
        assert unknown_count   == 0
        assert hard_count      == 6
    elif k == 4:
        assert tractable_count == 956
        assert unknown_count   == 0
        assert hard_count      == 1035
    elif k == 5:
        assert tractable_count == 1290862
        assert unknown_count   == 189
        assert hard_count      == 17375572

    return True
