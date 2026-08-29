import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns a list of booleans: [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok].
    """
    try:
        # 1. Boolean tuple/list
        if isinstance(witness, (list, tuple)) and len(witness) == 4 and all(isinstance(x, bool) for x in witness):
            return [witness[0], witness[1], witness[2], not witness[3]]

        # 2. Dictionary
        if isinstance(witness, dict):
            h1 = witness.get("H1", witness.get("h1", False))
            h2 = witness.get("H2", witness.get("h2", False))
            h3 = witness.get("H3", witness.get("h3", False))
            q = witness.get("Q", witness.get("q", True))
            return [bool(h1), bool(h2), bool(h3), not bool(q)]

        # 3. Object with H1, H2, H3, Q properties/methods
        if hasattr(witness, 'H1') or hasattr(witness, 'h1'):
            h1_attr = getattr(witness, 'H1', getattr(witness, 'h1', False))
            h1 = h1_attr() if callable(h1_attr) else h1_attr
            
            h2_attr = getattr(witness, 'H2', getattr(witness, 'h2', False))
            h2 = h2_attr() if callable(h2_attr) else h2_attr
            
            h3_attr = getattr(witness, 'H3', getattr(witness, 'h3', False))
            h3 = h3_attr() if callable(h3_attr) else h3_attr
            
            q_attr = getattr(witness, 'Q', getattr(witness, 'q', True))
            q = q_attr() if callable(q_attr) else q_attr
            
            return [bool(h1), bool(h2), bool(h3), not bool(q)]

        # 4. Mathematical tuple (L, K, G, O_K, O_L, P1, P2, p)
        if isinstance(witness, (list, tuple)) and len(witness) == 8:
            L, K, G, O_K, O_L, P1, P2, p = witness
            
            h1 = True
            if hasattr(L, 'is_galois'):
                h1 = L.is_galois(K)
                
            h2 = True
            
            h3 = True
            if hasattr(P1, 'is_prime'):
                h3 = P1.is_prime and P2.is_prime
                
            q = False
            if hasattr(G, 'orbit'):
                q = P2 in G.orbit(P1)
            elif isinstance(G, (list, tuple, set)):
                for sigma in G:
                    try:
                        if sigma(P1) == P2:
                            q = True
                            break
                    except Exception:
                        pass
            else:
                q = (P1 == P2)
                
            return [bool(h1), bool(h2), bool(h3), not bool(q)]

        # 5. Mathematical tuple (G, P1, P2, p)
        if isinstance(witness, (list, tuple)) and len(witness) == 4:
            G, P1, P2, p = witness
            from sympy.combinatorics import PermutationGroup
            h1 = isinstance(G, PermutationGroup)
            h2 = True
            h3 = (P1 in p) and (P2 in p)
            q = P2 in G.orbit(P1) if hasattr(G, 'orbit') else False
            return [bool(h1), bool(h2), bool(h3), not bool(q)]

        # 6. Object with descriptive methods
        h1 = h2 = h3 = False
        q = True
        
        if hasattr(witness, 'is_finite_galois_extension'):
            attr = witness.is_finite_galois_extension
            h1 = attr() if callable(attr) else attr
        elif hasattr(witness, 'is_galois'):
            attr = witness.is_galois
            h1 = attr() if callable(attr) else attr
            
        if hasattr(witness, 'are_rings_of_integers'):
            attr = witness.are_rings_of_integers
            h2 = attr() if callable(attr) else attr
        elif hasattr(witness, 'is_ring_of_integers'):
            attr = witness.is_ring_of_integers
            h2 = attr() if callable(attr) else attr
            
        if hasattr(witness, 'are_prime_ideals'):
            attr = witness.are_prime_ideals
            h3 = attr() if callable(attr) else attr
        elif hasattr(witness, 'is_prime'):
            attr = witness.is_prime
            h3 = attr() if callable(attr) else attr
            
        if hasattr(witness, 'exists_sigma'):
            attr = witness.exists_sigma
            q = attr() if callable(attr) else attr
        elif hasattr(witness, 'sigma_exists'):
            attr = witness.sigma_exists
            q = attr() if callable(attr) else attr
            
        return [bool(h1), bool(h2), bool(h3), not bool(q)]

    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension of number fields with Galois group G",
    "H_2: O_K and O_L are the rings of integers of K and L respectively",
    "H_3: P1 and P2 are prime ideals in O_L that intersect O_K at p",
    "¬Q: There does not exist sigma in G such that sigma(P1) = P2"
]

N_HYP = 3
NEG_Q_INDEX = 3