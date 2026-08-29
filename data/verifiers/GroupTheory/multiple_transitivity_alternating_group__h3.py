import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the conjecture:
    Hypotheses:
      - n is an integer greater than or equal to 3
      - A_n is the alternating group on n letters
    Conclusion:
      - The natural group action of A_n on X is (n-2)-transitive
    """
    # H_1: n is an integer greater than or equal to 3
    try:
        n = int(witness)
        h1_ok = (n >= 3) and (n == witness)
    except Exception:
        h1_ok = False

    # H_2: A_n is the alternating group on n letters
    # This is a definitional hypothesis, so if n is a valid integer, we can construct A_n.
    try:
        if h1_ok:
            A_n = AlternatingGroup(n)
            h2_ok = True
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: The natural group action of A_n on X is NOT (n-2)-transitive
    # We check if A_n is (n-2)-transitive.
    # A group G acting on {0, ..., n-1} is k-transitive if it acts transitively on the set of k-tuples of distinct elements.
    try:
        if h1_ok and h2_ok:
            k = n - 2
            elements = list(range(n))
            # Generate all k-tuples of distinct elements
            k_tuples = list(itertools.permutations(elements, k))
            
            if not k_tuples:
                is_k_transitive = True
            else:
                # We check if the orbit of the first k-tuple under A_n covers all k-tuples.
                # Since |A_n| can be large, we can just check if the size of the orbit equals the number of k-tuples.
                # The size of the orbit is |A_n| / |Stabilizer of the k-tuple|.
                # The stabilizer of a k-tuple in A_n consists of even permutations that fix the k elements pointwise.
                # There are n - k = 2 elements left.
                # The only permutations fixing the k elements are the identity and the transposition of the 2 remaining elements.
                # Since the transposition is odd, it is not in A_n.
                # Thus, the stabilizer in A_n is trivial (size 1).
                # The size of the orbit is |A_n| / 1 = n! / 2.
                # The number of k-tuples is n! / (n-k)! = n! / 2! = n! / 2.
                # Since the orbit size equals the number of k-tuples, A_n is ALWAYS (n-2)-transitive for n >= 3.
                # Wait, if it's always true, then neg_Q is always False.
                # Let's compute it explicitly for small n to be safe, or just use the mathematical fact.
                
                # Explicit check for n <= 6 to avoid timeout, though math guarantees it's True.
                if n <= 6:
                    target_tuple = k_tuples[0]
                    orbit = set()
                    for p in A_n.generate_dimino():
                        # Apply permutation to the tuple
                        mapped_tuple = tuple(p(x) for x in target_tuple)
                        orbit.add(mapped_tuple)
                    is_k_transitive = (len(orbit) == len(k_tuples))
                else:
                    # For n > 6, we rely on the mathematical fact that A_n is (n-2)-transitive.
                    is_k_transitive = True
            
            neg_q_ok = not is_k_transitive
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer greater than or equal to 3",
    "H_2: A_n is the alternating group on n letters",
    "¬Q: The natural group action of A_n on X is not (n-2)-transitive"
]

N_HYP = 2
NEG_Q_INDEX = 2