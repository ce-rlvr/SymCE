import sympy
from sympy.combinatorics import AlternatingGroup
import itertools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: n is an integer greater than or equal to 3",
    "H_2: X is the set {1, 2, ..., n}",
    "¬Q: The natural group action of A_n on X is NOT (n-2)-transitive"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      - n is an integer greater than or equal to 3
      - X is the set {1, 2, ..., n}
      
    Conclusion (must FAIL at the witness):
      The natural group action of A_n on X is (n-2)-transitive
    """
    try:
        n = int(witness)
        h1 = n >= 3
    except Exception:
        h1 = False

    # The second hypothesis "X is the set {1, 2, ..., n}" is a definitional setup
    # for the conclusion, so we just consider it trivially true if n is a valid integer.
    h2 = h1

    # Check if the conclusion fails (neg_Q_ok = True)
    # The conclusion is that A_n is (n-2)-transitive.
    # A group action is k-transitive if it acts transitively on k-tuples of distinct elements.
    neg_q = False
    try:
        if h1:
            k = n - 2
            if k <= 0:
                neg_q = False
            else:
                # We check if A_n is k-transitive.
                # It is k-transitive iff for any two k-tuples of distinct elements,
                # there is an even permutation mapping one to the other.
                # We can check this by verifying if the number of orbits of A_n on k-tuples is 1.
                # Or simply by trying to map a fixed k-tuple to all other k-tuples.
                
                # For n >= 3, A_n is actually ALWAYS (n-2)-transitive.
                # Wait, if A_n is always (n-2)-transitive, then neg_q would be False.
                # However, we must evaluate the condition exactly as stated.
                # Let's compute it directly for the given n.
                
                G = AlternatingGroup(n)
                elements = list(range(n))
                k_tuples = list(itertools.permutations(elements, k))
                
                if not k_tuples:
                    is_k_transitive = True
                else:
                    t1 = k_tuples[0]
                    is_k_transitive = True
                    
                    # We only need to check if the orbit of t1 covers all k_tuples
                    orbit = set()
                    for g in G.elements:
                        # Apply permutation g to tuple t1
                        mapped_t1 = tuple(g(x) for x in t1)
                        orbit.add(mapped_t1)
                        
                    if len(orbit) < len(k_tuples):
                        is_k_transitive = False
                        
                neg_q = not is_k_transitive
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]