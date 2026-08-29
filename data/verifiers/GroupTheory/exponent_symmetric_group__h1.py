import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = SymmetricGroup(4) # AlternatingGroup is not directly imported, but we define standard objects
Z2 = SymmetricGroup(2)
trivial = SymmetricGroup(1)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    
    Hypothesis: Let S_n be the symmetric group on n letters.
    Conclusion: The exponent of S_n is the least common multiple of the integers 1, 2, ..., n.
    """
    h1_ok = False
    n = None
    
    # Check if the witness is an integer representing n, or a symmetric group
    try:
        if isinstance(witness, int):
            if witness >= 1:
                h1_ok = True
                n = witness
        elif hasattr(witness, 'is_symmetric_group') and witness.is_symmetric_group:
            h1_ok = True
            n = witness.degree
    except Exception:
        pass

    neg_q_ok = False
    try:
        if h1_ok and n is not None:
            # Calculate the exponent of S_n
            # The exponent is the least common multiple of the orders of all elements in S_n.
            # The order of an element is the lcm of the lengths of its disjoint cycles.
            # We can find the exponent by taking the lcm of all possible cycle lengths up to n.
            def partitions(n):
                a = [0 for i in range(n + 1)]
                k = 1
                y = n - 1
                while k != 0:
                    x = a[k - 1] + 1
                    k -= 1
                    while 2 * x <= y:
                        a[k] = x
                        y -= x
                        k += 1
                    l = k + 1
                    while x <= y:
                        a[k] = x
                        a[l] = y
                        yield a[:k + 2]
                        x += 1
                        y -= 1
                    a[k] = x + y
                    y = x + y - 1
                    yield a[:k + 1]
            
            # If n is very large, we avoid computing partitions to prevent timeout,
            # but for reasonable witnesses, we compute the exact exponent of the group.
            if n <= 50:
                exp_Sn = 1
                for p in partitions(n):
                    l = 1
                    for x in p:
                        l = math.lcm(l, x)
                    exp_Sn = math.lcm(exp_Sn, l)
            else:
                # Fallback for large n (though mathematically exp_Sn is always lcm(1..n))
                exp_Sn = 1
                for i in range(1, n + 1):
                    exp_Sn = math.lcm(exp_Sn, i)
            
            # Calculate the least common multiple of the integers 1, 2, ..., n
            lcm_n = 1
            for i in range(1, n + 1):
                lcm_n = math.lcm(lcm_n, i)
                
            # The negated conclusion is True if the exponent is NOT equal to lcm(1..n)
            neg_q_ok = (exp_Sn != lcm_n)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let S_n be the symmetric group on n letters",
    "¬Q: The exponent of S_n is not the least common multiple of the integers 1, 2, ..., n"
]

N_HYP = 1
NEG_Q_INDEX = 1