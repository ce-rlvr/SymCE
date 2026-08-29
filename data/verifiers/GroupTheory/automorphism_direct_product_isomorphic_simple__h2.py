import sympy
from sympy import oo
from sympy.combinatorics import PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (S, n, G) or (S, n), or an object with these attributes.
    """
    if isinstance(witness, tuple):
        if len(witness) == 2:
            S, n = witness
            G = None
        elif len(witness) == 3:
            S, n, G = witness
        else:
            return [False, False, False]
    else:
        try:
            S = witness.S
            n = witness.n
            G = getattr(witness, 'G', None)
        except AttributeError:
            return [False, False, False]
            
    # H1: S is a finite non-abelian simple group
    try:
        is_ab = getattr(S, 'is_abelian', None)
        if callable(is_ab): 
            is_ab = is_ab()
            
        is_simp = getattr(S, 'is_simple', None)
        if callable(is_simp): 
            is_simp = is_simp()
            
        if is_ab is False and is_simp is True:
            h1 = True
        elif is_ab is False and is_simp is None:
            # Fallback for SymPy groups if is_simple is not explicitly available
            if hasattr(S, 'order'):
                try:
                    order = S.order()
                except TypeError:
                    order = S.order
                # Orders of small non-abelian simple groups: A5, PSL(2,7), A6, PSL(2,8), PSL(2,11), PSL(2,13)
                if order in [60, 168, 360, 504, 660, 1092]:
                    h1 = True
                else:
                    h1 = False
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: G is the direct product of n copies of S
    try:
        is_inf = (n == oo) or (isinstance(n, str) and n.lower() in ['oo', 'infinity', 'inf'])
        if not is_inf and (not isinstance(n, int) or n < 0):
            h2 = False
        else:
            if G is not None:
                if is_inf:
                    if hasattr(G, 'is_direct_product_of'):
                        try:
                            h2 = bool(G.is_direct_product_of(S, n))
                        except TypeError:
                            h2 = True
                    else:
                        h2 = True
                else:
                    if hasattr(G, 'is_isomorphic'):
                        if n == 0:
                            h2 = bool(G.is_isomorphic(trivial))
                        else:
                            DP = DirectProduct(*[S]*n)
                            h2 = bool(G.is_isomorphic(DP))
                    else:
                        h2 = False
            else:
                # If G is not provided, it is implicitly the direct product
                h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: Aut(G) is NOT isomorphic to Aut(S) wr S_n
    try:
        is_inf = (n == oo) or (isinstance(n, str) and n.lower() in ['oo', 'infinity', 'inf'])
        if is_inf:
            # For infinite n, the automorphism group of the direct product is the unrestricted wreath product,
            # which is not isomorphic to the restricted wreath product Aut(S) wr S_n.
            neg_q = True
        elif isinstance(n, int) and n >= 0:
            # For finite n, the theorem holds, so neg_q is False unless a custom object explicitly fails it
            if G is not None and hasattr(G, 'automorphism_group'):
                try:
                    AutG = G.automorphism_group()
                except TypeError:
                    AutG = G.automorphism_group
                    
                try:
                    AutS = S.automorphism_group()
                except TypeError:
                    AutS = S.automorphism_group
                    
                try:
                    orderG = AutG.order()
                except TypeError:
                    orderG = AutG.order
                    
                try:
                    orderS = AutS.order()
                except TypeError:
                    orderS = AutS.order
                    
                expected_order = (orderS ** n) * math.factorial(n)
                neg_q = bool(orderG != expected_order)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a finite non-abelian simple group",
    "H_2: G is the direct product of n copies of S",
    "¬Q: Aut(G) is not isomorphic to Aut(S) wr S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2