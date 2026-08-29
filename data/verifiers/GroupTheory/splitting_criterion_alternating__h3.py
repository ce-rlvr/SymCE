import math
from sympy.combinatorics import Permutation

# Top-level setup
# No specific named objects are required for this conjecture's witness,
# as the witness is expected to be a tuple (n, x) or a Permutation x.

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks the hypotheses and the negated conclusion.
    The witness is expected to be a tuple (n, x) where n is an integer and x is a sympy Permutation,
    or just a Permutation x (in which case n is inferred as x.size).
    """
    try:
        if isinstance(witness, tuple):
            n, x = witness
        else:
            x = witness
            n = x.size
    except Exception:
        return [False, False, False, False]
        
    # H_1: n is an integer greater than 1
    try:
        h1 = isinstance(n, int) and n > 1
    except Exception:
        h1 = False
        
    # H_2: S_n is the symmetric group on n letters
    # We verify this by checking if x is a valid permutation on at most n letters.
    try:
        h2 = isinstance(x, Permutation) and x.size <= n
    except Exception:
        h2 = False
        
    # H_3: x is an element of A_n
    try:
        h3 = h2 and x.is_even
    except Exception:
        h3 = False
        
    # ¬Q: The conclusion fails at the witness.
    # Conclusion: The conjugacy class of x in S_n splits into two distinct conjugacy classes 
    # of equal size in A_n if and only if the centralizer of x in S_n is a subgroup of A_n.
    try:
        if not h2:
            neg_q = False
        else:
            # Compute the cycle lengths of x in S_n (including 1-cycles for fixed points)
            cycle_lengths = [len(c) for c in x.cyclic_form]
            ones = n - sum(cycle_lengths)
            if ones < 0:
                neg_q = False
            else:
                cycle_lengths.extend([1] * ones)
                
                # Q_cond: The centralizer of x in S_n is a subgroup of A_n.
                # By standard group theory, this holds if and only if the cycle type of x 
                # consists entirely of distinct odd integers.
                all_odd = all(l % 2 == 1 for l in cycle_lengths)
                distinct = len(cycle_lengths) == len(set(cycle_lengths))
                Q_cond = all_odd and distinct
                
                # P_cond: The conjugacy class of x in S_n splits into two distinct conjugacy 
                # classes of equal size in A_n.
                # The size of the conjugacy class in S_n is n! / |C_{S_n}(x)|.
                # The size of the conjugacy class in A_n is (n! / 2) / |C_{A_n}(x)|.
                # It splits into two distinct classes of equal size iff |C_{A_n}(x)| == |C_{S_n}(x)|,
                # which is equivalent to C_{S_n}(x) <= A_n.
                # Thus, P_cond is mathematically equivalent to Q_cond.
                P_cond = Q_cond
                
                # The conclusion is the biconditional P_cond <-> Q_cond.
                # We want the negation of the conclusion.
                neg_q = not (P_cond == Q_cond)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: S_n is the symmetric group on n letters",
    "H_3: x is an element of A_n",
    "¬Q: The conjugacy class of x in S_n splits into two distinct conjugacy classes of equal size in A_n if and only if the centralizer of x in S_n is a subgroup of A_n is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3