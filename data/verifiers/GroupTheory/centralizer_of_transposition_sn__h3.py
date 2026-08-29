import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, PermutationGroup
import sympy.combinatorics

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (n, tau) where n is an integer >= 2 and 
    tau is a Permutation in S_n.
    """
    try:
        n, tau = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n >= 2 is an integer
    try:
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False
        
    # H_2: tau is an element of S_n
    try:
        if not isinstance(tau, Permutation):
            h2 = False
        else:
            support = tau.support() if callable(tau.support) else tau.support
            h2 = max(support or [-1]) < n
    except Exception:
        h2 = False
        
    # neg_Q: The centralizer of tau in S_n is NOT isomorphic to C_2 x S_{n-2}
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            Sn = SymmetricGroup(n)
            
            # Normalize tau to size n
            cyclic_form = tau.cyclic_form() if callable(tau.cyclic_form) else tau.cyclic_form
            if not cyclic_form:
                tau_n = Permutation(size=n)
            else:
                tau_n = Permutation(cyclic_form, size=n)
            
            # Compute the centralizer of tau in S_n
            try:
                cent_group = Sn.centralizer(PermutationGroup([tau_n]))
            except Exception:
                try:
                    cent_group = Sn.centralizer(tau_n)
                except Exception:
                    if n > 6:
                        raise ValueError("n too large for fallback iteration")
                    cent_elements = [p for p in Sn.generate() if p * tau_n == tau_n * p]
                    cent_group = PermutationGroup(cent_elements)
            
            # Construct the target group C_2 x S_{n-2}
            # C_2 acts on {0, 1}, S_{n-2} acts on {2, ..., n-1}
            gens = [Permutation(0, 1, size=n)]
            if n >= 4:
                gens.append(Permutation(2, 3, size=n))
                if n >= 5:
                    gens.append(Permutation(*list(range(2, n)), size=n))
                    
            target_group = PermutationGroup(gens)
            
            # Check isomorphism
            order_cent = cent_group.order() if callable(cent_group.order) else cent_group.order
            order_target = target_group.order() if callable(target_group.order) else target_group.order
            
            if order_cent != order_target:
                neg_q = True
            else:
                try:
                    neg_q = not cent_group.is_isomorphic(target_group)
                except Exception:
                    # Fallback for isomorphism check using element orders
                    orders1 = sorted([g.order() if callable(g.order) else g.order for g in cent_group.generate()])
                    orders2 = sorted([g.order() if callable(g.order) else g.order for g in target_group.generate()])
                    neg_q = (orders1 != orders2)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: tau is an element of S_n",
    "¬Q: The centralizer of tau in S_n is not isomorphic to C_2 x S_{n-2}"
]

N_HYP = 2
NEG_Q_INDEX = 2