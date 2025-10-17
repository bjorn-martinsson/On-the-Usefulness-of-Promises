from collections.abc import Callable

"""
A home made SAT-solver used to find obstruction to functions
in a given Family. This is based only on unit-propagation.

The reason why we use our own SAT-solver is that generating 
the entire SAT instance at once can be increadibly slow and 
use large amount of memory. By implementing our own SAT-solver 
we are able to mostly avoid this issue by avoiding to generate 
clauses that we already know to be satisfied.

The reason why we only use unit propagation instead a full 
SAT-solver is that it is simpler, faster, and from our testing 
ultimately does not seem to affect the result.
"""

class Trie:
    def __init__(self):
        self.root = {}

    def add(self, S):
        node = self.root
        for c in S:
            if c not in node:
                node[c] = node = {}
            else:
                node = node[c]

def find_obstruction(pattern: list[int], zero_weights: list[tuple[int]], ktries: list[list[Trie]]) -> bool | None:
    m = len(pattern)
    assert m == len(ktries[0])
    assert all(m == len(weight) for weight in zero_weights)

    assert all(0 <= w <= p for weight in zero_weights for p,w in zip(pattern, weight))
    one_weights = {tuple(pattern[i] - weight[i] for i in range(m)) for weight in zero_weights}
    zero_weights = set(zero_weights)

    if zero_weights & one_weights:
        raise ValueError('Function given is not foldable')

    k = len(ktries)
    
    function_size = 1
    for pat in pattern:
        function_size *= pat + 1

    from itertools import product
    
    from collections import defaultdict
    waiting_list = defaultdict(list)

    DFS = [(tuple(trie.root for trie in ktries[i]),  0) for i in range(k)]

    while DFS:
        nodes, dist = DFS.pop()
        if dist == k:
            # Obstruction found!
            return True

        for weight in product(*map(iter, nodes)):
            if weight in zero_weights:
                # f of row in matrix is 0, continue with next row
                DFS.append((tuple(node[w] for node,w in zip(nodes, weight)), dist + 1))
            elif weight in one_weights:
                # f of row in matrix is 1, cannot be obstruction
                pass
            elif dist == k - 1:
                # f of last row in matrix is unknown, force f of last row to be 1
                # (unit propagation step)
                nweight = tuple(pattern[i] - weight[i] for i in range(m)) 
                zero_weights.add(nweight)
                one_weights.add(weight)
                DFS += waiting_list[nweight]
                del waiting_list[nweight]
                del waiting_list[weight]

#                if len(zero_weights) == function_size // 2:
#                    print('Unit propagation fixed all function values.', flush=True)
            else:
                # f-value of current row is unknown, wait for more information
                waiting_list[weight].append((tuple(node[w] for node,w in zip(nodes, weight)), dist + 1))

    if len(zero_weights) == function_size//2:
        # Polymorhpism from family exists
        return False

    # Unit propagation did not give enough information
    return None

def has_obstruction(pattern: list[int], predicate: list[str], family: Callable[[tuple[int]], int | None]) -> bool | None:
    """
    This answers the question if there exists an obstruction matrix for every function in a family of Boolean functions.

    It returns: 
    * False if the polymorphism of fiPCSP(predicate, OR) contains at least one function of the family.
    * None if it is unnable to verify whether or not the polymorphisms of fiPCSP(predicate, OR) contain at least one function of the family.
    * True if the polymorphism of fiPCSP(predicate, OR) contains no functions from the family.

    The variable pattern is a list of integers that describe the sizes of "blocks" used by the family.
    (Same notition of blocks as in block-symmetric)
    The reason this is used is that it can significantly boost performance.
    """
    from itertools import combinations
    from itertools import product
    from itertools import combinations_with_replacement
    def adder(*A):
        ret = [0] * len(A[0])
        for B in A:
            for i,b in enumerate(B):
                ret[i] += b
        return ret

    k = len(predicate[0])
    ktries = [[] for _ in range(k)]
    for pat in pattern:
        for i in range(k):
            ktries[i].append(Trie())
        
        for A in combinations_with_replacement(predicate, pat):
            weight = adder(*([int(c) for c in bitstring] for bitstring in A))
            for i in range(k):
                # Swap so i is last
                weight[i],weight[-1] = weight[-1],weight[i]
                ktries[i][-1].add(weight)
                weight[i],weight[-1] = weight[-1],weight[i]

    weight = product(*(range(pat + 1) for pat in pattern))
    zero_weights = [w for w in weight if family(w) == 0]
    return find_obstruction(pattern, zero_weights, ktries)
