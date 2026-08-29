import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import totient
import itertools

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (n, sigma)
    where n is an integer >= 3, and sigma is a Permutation in S_n.
    """
    try:
        n, sigma = witness
    except Exception:
        return [False, False, False]

    # H_1: n >= 3 is an integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) >= 3
    except Exception:
        h1 = False

    # H_2: sigma is an element of S_n
    try:
        h2 = isinstance(sigma, Permutation) and sigma.size <= int(n)
    except Exception:
        h2 = False

    # ¬Q: The normalizer of <sigma> in S_n does NOT have order n * phi(n)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n_int = int(n)
            if n_int > 8:
                # Prevent timeout for unreasonably large n
                neg_q = False
            else:
                # Ensure sigma is represented as a permutation of size exactly n
                array_form = sigma.array_form
                if len(array_form) < n_int:
                    array_form = array_form + list(range(len(array_form), n_int))
                sigma_n = Permutation(array_form)
                
                # Generate the subgroup H = <sigma>
                H_elements = set()
                curr = sigma_n
                order = sigma_n.order()
                for _ in range(order):
                    H_elements.add(curr)
                    curr = curr * sigma_n
                    
                # Count the order of the normalizer of H in S_n
                norm_order = 0
                for p in itertools.permutations(range(n_int)):
                    g = Permutation(list(p))
                    # g normalizes H iff g * sigma * g^-1 is in H
                    conj = g * sigma_n * ~g
                    if conj in H_elements:
                        norm_order += 1
                        
                expected = n_int * totient(n_int)
                neg_q = norm_order != expected
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: sigma is an element of S_n",
    "¬Q: The normalizer of <sigma> in S_n does not have order n * phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2