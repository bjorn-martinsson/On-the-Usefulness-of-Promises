"""
    Checks if fiPCSP(A, OR) does not contain an ANDNOR.

    Based on sub-section A.7
"""

def check(predicate: list[str]) -> bool:
    if not predicate:
        return False
    k = len(predicate[0])
    predicate_tuples = [tuple(int(c) for c in assign) for assign in predicate]

    # Create an obstruction matrix for ANDNOR
    for bitstring0 in predicate:
        for bitstring1 in predicate:
            col0 = [int(x) for x in bitstring0]
            col1 = [int(x) for x in bitstring1]

            if any(col0[i] == col1[i] == 1 for i in range(k)):
                continue
        
            # rows i where col0[i]=1 and col1[i]=0 need to be 1 in all other columns
            ones = []
            for i in range(k):
                if col0[i]==1 and col1[i]==0:
                    ones.append(i)
        
            # The set of assignment assign where assign[i]=1 for all i in ones.
            filtered_predicate = [assign for assign in predicate_tuples if all(assign[i] == 1 for i in ones)]

            # Edge case where it is impossible to create obstruction matrix
            if not filtered_predicate:
                continue
            
            # Go over all rows i
            for i in range(k):
                # If row starts with a 0 1
                if col0[i] == 0 and col1[i] == 1:
                    # To construct an obstruction, there needs
                    # to be one more 1 on the row
                    for assign in filtered_predicate:
                        if assign[i] == 1:
                            break
                    else:
                        break
            else:
                return True
    return False
