import itertools
from sympy.combinatorics import AlternatingGroup

# Top-level setup
# No specific named objects are needed for this conjecture since the witness is an integer n.

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    
    Hypotheses:
      1. n is an integer with n >= 3.
      2. A_n is the alternating group of degree n. (Implicitly checked by constructing A_n)
      
    Conclusion (must FAIL):
      The natural action of A_n on X is (n-2)-transitive.
    """
    # Hypothesis 1: n is an integer with n >= 3
    try:
        n = int(witness)
        h1_ok = (n >= 3 and n == witness)
    except Exception:
        h1_ok = False

    # Hypothesis 2: A_n is the alternating group of degree n
    # This is a definitional hypothesis, so it holds trivially if n is a valid integer.
    h2_ok = h1_ok

    # Negated Conclusion: The natural action of A_n on X is NOT (n-2)-transitive.
    # We evaluate whether A_n is (n-2)-transitive. If it is NOT, then neg_Q is True.
    neg_q = False
    if h1_ok:
        try:
            k = n - 2
            G = AlternatingGroup(n)
            
            # Generate all k-tuples of distinct elements from {0, 1, ..., n-1}
            elements = list(range(n))
            k_tuples = list(itertools.permutations(elements, k))
            
            if not k_tuples:
                # If k=0, it's trivially 0-transitive, so neg_q = False
                neg_q = False
            else:
                # To check k-transitivity, we just need to see if the orbit of the first tuple
                # under the action of A_n covers all k-tuples.
                start_tuple = k_tuples[0]
                orbit = set()
                
                for g in G.elements:
                    # Apply permutation g to the start_tuple
                    mapped_tuple = tuple(g(x) for x in start_tuple)
                    orbit.add(mapped_tuple)
                
                # If the orbit size equals the total number of k-tuples, it is k-transitive.
                # The conclusion FAILS (neg_q is True) if the orbit does not cover all k-tuples.
                is_k_transitive = (len(orbit) == len(k_tuples))
                neg_q = not is_k_transitive
        except Exception:
            neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 3",
    "H_2: A_n is the alternating group of degree n",
    "¬Q: The natural action of A_n on X is NOT (n-2)-transitive"
]

N_HYP = 2
NEG_Q_INDEX = 2