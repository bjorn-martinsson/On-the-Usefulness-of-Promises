from bitset import bitset
import parse_tables
import verification
from functools import lru_cache as memoization

"""
    This file contains functions for verifying correctness of the tables corresponding
    to promise usefulness/uselessness.
"""

@memoization
def get_tables(k: int) -> tuple[list[list[str]]]:
    # Table with "hardest" promise useful predicates
    maximal_promise_useful = parse_tables.read('tables/maximal_promise_useful_k%d.txt' % k)
    
    # Table  with "easiest" promise useless predicates
    minimal_promise_useless = parse_tables.read('tables/minimal_promise_useless_k%d.txt' % k)
    
    # Table with "hardest" promise unknown predicates
    maximal_promise_unknown = parse_tables.read('tables/maximal_promise_unknown_k%d.txt' % k)
    
    # Table with "easiest" promise unknown predicates
    minimal_promise_unknown = parse_tables.read('tables/minimal_promise_unknown_k%d.txt' % k)
    
    return maximal_promise_useful, minimal_promise_useless, maximal_promise_unknown, minimal_promise_unknown

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

def xor(bitstring1: str, bitstring2: str) -> str:
    return ''.join('0' if c1==c2 else '1' for c1,c2 in zip(bitstring1, bitstring2))

def all_xors(predicate: list[str]) -> list[list[str]]:
    if not predicate:
        return []

    k = len(predicate[0])
    
    out = []
    for bitstring in parse_tables.all_bitstrings(k):
        predicate2 = [xor(bitstring, b) for b in predicate]
        predicate2.sort()
        if predicate2 not in out:
            out.append(predicate2)
    return out

def predicate_to_bitmask(predicate: list[str]) -> int:
    out = 0
    for assign in predicate:
        out |= 1 << int(assign, 2)
    return out

@memoization
def get_bitsets(k: int) -> tuple[bitset]:
    maximal_promise_useful, minimal_promise_useless, maximal_promise_unknown, minimal_promise_unknown = get_tables(k)
    m = 2**(2**k)
    
    # Find all promise useful predicates
    promise_useful_bitset = bitset(m)
    
    # Fill in the maximal promise useful predicates
    for predicate in maximal_promise_useful:
        for predicate2 in all_permutations(predicate):
            for predicate3 in all_xors(predicate2):
                p = predicate_to_bitmask(predicate3)
                promise_useful_bitset[p] = 1
    
    # Fill in implications
    for i in range(m)[::-1]:
        if promise_useful_bitset[i]:
            for bit in range(2**k):
                i2 = i & ~(1 << bit)
                promise_useful_bitset[i2] = 1
    
    # Find all promise useless predicates
    promise_useless_bitset = bitset(m)
    
    # Fill in the minimal promise useless predicates
    for predicate in minimal_promise_useless:
        for predicate2 in all_permutations(predicate):
            for predicate3 in all_xors(predicate2):
                p = predicate_to_bitmask(predicate3)
                promise_useless_bitset[p] = 1
    
    # Fill in implications
    for i in range(m):
        if promise_useless_bitset[i]:
            for bit in range(2**k):
                i2 = i | (1 << bit)
                promise_useless_bitset[i2] = 1
    # Predicate with all bitstrings is not allowed
    promise_useless_bitset[m - 1] = 0
    
    # Find all promise useful + unknown predicates
    promise_useful_and_unknown_bitset = promise_useful_bitset.copy()
    
    # Fill in the maximal promise unknown predicates
    for predicate in maximal_promise_unknown:
        for predicate2 in all_permutations(predicate):
            for predicate3 in all_xors(predicate2):
                p = predicate_to_bitmask(predicate3)
                promise_useful_and_unknown_bitset[p] = 1
    
    # Fill in implications
    for i in range(m)[::-1]:
        if promise_useful_and_unknown_bitset[i]:
            for bit in range(2**k):
                i2 = i & ~(1 << bit)
                promise_useful_and_unknown_bitset[i2] = 1
    
    # Find all promise useless + unknown predicates
    promise_useless_and_unknown_bitset = promise_useless_bitset.copy()
    
    # Fill in the minimal promise unknown predicates
    for predicate in minimal_promise_unknown:
        for predicate2 in all_permutations(predicate):
            for predicate3 in all_xors(predicate2):
                p = predicate_to_bitmask(predicate3)
                promise_useless_and_unknown_bitset[p] = 1
    # Predicate with all bitstrings is not allowed
    promise_useless_and_unknown_bitset[m - 1] = 0

    # Fill in implications
    for i in range(m):
        if promise_useless_and_unknown_bitset[i]:
            for bit in range(2**k):
                i2 = i | (1 << bit)
                promise_useless_and_unknown_bitset[i2] = 1

    # Promise unknown predicates lie in the intersection of the two bitsets
    promise_unknown_bitset = promise_useful_and_unknown_bitset & promise_useless_and_unknown_bitset
    return promise_useful_bitset, promise_unknown_bitset, promise_useless_bitset


def verify_coverage(k: int) -> bool:
    """
        The minimal/maximal tables should cover all possible predicates.
        This verifies that all predicates are covered, and that the minimal/maximal
        tables are actually minimal/maximal.
    """

    maximal_promise_useful, minimal_promise_useless, maximal_promise_unknown, minimal_promise_unknown = get_tables(k)
    promise_useful_bitset, promise_unknown_bitset, promise_useless_bitset = get_bitsets(k)
    m = 2**(2**k) # Size of the bitsets

    # Check that none of the 3 regions promise-(useful, useless, unknown) intersect
    assert (promise_useful_bitset & promise_unknown_bitset).sum() == 0
    assert (promise_useful_bitset & promise_useless_bitset).sum() == 0
    assert (promise_unknown_bitset & promise_useless_bitset).sum() == 0

    # Check that their union is everything
    
    assert (promise_useful_bitset).sum() + (promise_unknown_bitset).sum() + (promise_useless_bitset).sum() == m - 1

    # Verify maximality of maximal_tractable
    for predicate in maximal_promise_useful:
        # Check that any larger predicate is not promise useful
        p = predicate_to_bitmask(predicate)
        assert promise_useful_bitset[p]
        for bit in range(2**k):
            if p & (1 << bit) == 0:
                assert not promise_useful_bitset[p | (1 << bit)]

    # Verify minimality of minimal_promise_useless
    for predicate in minimal_promise_useless:
        # Check that any smaller predicate is not promise useless
        p = predicate_to_bitmask(predicate)
        assert promise_useless_bitset[p]
        for bit in range(2**k):
            if p & (1 << bit):
                assert not promise_useless_bitset[p | ~(1 << bit)]

    # Verify maximality of maximal_promise_unknown
    for predicate in maximal_promise_unknown:
        # Check that any larger predicate is not unknown
        p = predicate_to_bitmask(predicate)
        assert promise_unknown_bitset[p]
        for bit in range(2**k):
            if p & (1 << bit) == 0:
                assert not promise_unknown_bitset[p | (1 << bit)]
    
    # Verify minimality of minimal_promise_unknown
    for predicate in minimal_promise_unknown:
        # Check that any smaller predicate is not unknown
        p = predicate_to_bitmask(predicate)
        assert promise_unknown_bitset[p]
        for bit in range(2**k):
            if p & (1 << bit):
                assert not promise_unknown_bitset[p | ~(1 << bit)]

    return True


def verify_promise_usefulness(k: int) -> bool:
    """
    Verifies that: 
        1. There is an assignment b such that predicate xor b is tractable, for predicate in maximal_promise_useful
        2. There is no assignment b such that predicate xor b is tractable for predicate in minimal_promise_useless,
           maximal_promise_unknown and minimal_promise_unknown.

    """
    tractable_bitset, unknown_bitset, hard_bitset = verification.get_bitsets(k)
    maximal_promise_useful, minimal_promise_useless, maximal_promise_unknown, minimal_promise_unknown = get_tables(k)
    
    for predicate in maximal_promise_useful:
        for predicate2 in all_xors(predicate):
            p = predicate_to_bitmask(predicate2)
            if p&1 == 0 and tractable_bitset[p]:
                break
        else:
            assert False
    
    for predicate in minimal_promise_useless + maximal_promise_unknown + minimal_promise_unknown:
        for predicate2 in all_xors(predicate):
            p = predicate_to_bitmask(predicate2)
            if p&1 == 0:
                assert not tractable_bitset[p]
    
    return True

def verify_promise_uselessness(k: int) -> bool:
    """
    Verifies that: 
        1. For all assignments b the predicate xor b is hard, for predicate in minimal_promise_useless
        2. There exist some assignment b such that the predicate xor b is not hard, for predicate in 
           maximal_promise_useful, maximal_promise_unknown and minimal_promise_unknown

    """
    tractable_bitset, unknown_bitset, hard_bitset = verification.get_bitsets(k)
    maximal_promise_useful, minimal_promise_useless, maximal_promise_unknown, minimal_promise_unknown = get_tables(k)
    
    for predicate in minimal_promise_useless:
        for predicate2 in all_xors(predicate):
            p = predicate_to_bitmask(predicate2)
            if p&1 == 0:
                assert hard_bitset[p]
    
    for predicate in maximal_promise_useful + maximal_promise_unknown + minimal_promise_unknown:
        for predicate2 in all_xors(predicate):
            p = predicate_to_bitmask(predicate2)
            if p&1 == 0 and not hard_bitset[p]:
                break
        else:
            assert False
    
    return True


def verify_representative_lexographically_smallest(k: int) -> bool:
    """
    Verifies that the representatives are lexographically smallest with respect to permutations
    and with respect to xor with arbitrary bitstrings.
    Additionally verifies that representatives in each table are given in lexiographical order.
    """
    maximal_promise_useful, minimal_promise_useless, maximal_promise_unknown, minimal_promise_unknown = get_tables(k)
    for predicate in maximal_promise_useful + minimal_promise_useless + maximal_promise_unknown + minimal_promise_unknown:
        p1 = predicate_to_bitmask(predicate)
        for predicate2 in all_permutations(predicate):
            for predicate3 in all_xors(predicate2):
                p3 = predicate_to_bitmask(predicate3)
                assert p1 <= p3
    
    for predicates in maximal_promise_useful, minimal_promise_useless, maximal_promise_unknown, minimal_promise_unknown:
        prev = None
        for predicate in predicates:
            p = predicate_to_bitmask(predicate)
            assert prev == None or prev < p
            prev = p

    return True

@memoization
def get_representatives(k: int) -> bool:
    """
    Computes all representatives with respect to permutations and xor with bitstrings.
    """

    # Uses bitmasks instead of bitstrings for enhanced performance
    import itertools
    permutations = itertools.permutations(range(k)) 
    maps = []
    for permutation in permutations:
        for xor_bitstring in parse_tables.all_bitstrings(k):
            mapping = [0] * 2**k
            for bitstring in parse_tables.all_bitstrings(k):
                permuted_bitstring = ''.join(bitstring[i] for i in permutation)
                permuted_and_xored_bitstring = ''.join('1' if c1!=c2 else '0' for c1,c2 in zip(permuted_bitstring, xor_bitstring))
                mapping[int(bitstring, 2)] = int(permuted_and_xored_bitstring, 2)

            # Avoid duplicates
            if mapping not in maps:
                maps.append(mapping)

    def apply_map(p, mapping):
        q = 0
        for i in range(2**k):
            q |= ((p >> i) & 1) << mapping[i]
        return q

    representatives = []
    m = 2**(2**k)
    found = bitset(m)
    for p in range(1, m - 1):
        if found[p]:
            continue
        representatives.append(p)
        for mapping in maps:
            q = apply_map(p, mapping)
            found[q] =1
    
    return representatives

def verify_counts(k: int) -> bool:
    """
    Checks that the counts of promise-useful/unknown/useless predicate matches the numbers in the paper
    """
    promise_useful_bitset, promise_unknown_bitset, promise_useless_bitset = get_bitsets(k)
    representatives = get_representatives(k)

    promise_useful_count = promise_unknown_count = promise_useless_count = 0
    for p in representatives:
        if promise_useful_bitset[p]:
            promise_useful_count += 1
        if promise_unknown_bitset[p]:
            promise_unknown_count += 1
        if promise_useless_bitset[p]:
            promise_useless_count += 1

    assert len(representatives) == promise_useful_count + promise_unknown_count + promise_useless_count
    
    if k == 2:
        assert promise_useful_count  == 4
        assert promise_unknown_count == 0
        assert promise_useless_count == 0
    elif k == 3:
        assert promise_useful_count  == 16
        assert promise_unknown_count == 0
        assert promise_useless_count == 4
    elif k == 4:
        assert promise_useful_count  == 230
        assert promise_unknown_count == 0
        assert promise_useless_count == 170
    elif k == 5:
        assert promise_useful_count  == 156135
        assert promise_unknown_count == 59
        assert promise_useless_count == 1071962

    return True
