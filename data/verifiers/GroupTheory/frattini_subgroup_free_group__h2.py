import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    # H_1: F is a free group
    # neg_Q: The Frattini subgroup of F is not the trivial group
    
    try:
        h1 = False
        try:
            from sympy.combinatorics.free_groups import FreeGroup
            if isinstance(witness, FreeGroup):
                h1 = True
        except ImportError:
            pass
            
        try:
            from sympy.combinatorics.fp_groups import FpGroup
            if isinstance(witness, FpGroup) and len(witness.relators) == 0:
                h1 = True
        except ImportError:
            pass
            
        if not h1:
            order = witness.order() if callable(getattr(witness, 'order', None)) else getattr(witness, 'order', None)
            if order == 1:
                h1 = True
    except Exception:
        h1 = False

    try:
        is_trivial = False
        is_free = False
        
        try:
            from sympy.combinatorics.free_groups import FreeGroup
            if isinstance(witness, FreeGroup):
                is_free = True
        except ImportError:
            pass
            
        try:
            from sympy.combinatorics.fp_groups import FpGroup
            if isinstance(witness, FpGroup) and len(witness.relators) == 0:
                is_free = True
        except ImportError:
            pass
            
        if is_free:
            is_trivial = True
        else:
            order = witness.order() if callable(getattr(witness, 'order', None)) else getattr(witness, 'order', None)
            if order == 1:
                is_trivial = True
            elif order is not None:
                is_ab = False
                if hasattr(witness, 'is_abelian'):
                    is_ab = witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian
                
                factors = factorint(order)
                
                if is_ab:
                    # An abelian group has a trivial Frattini subgroup iff it is elementary abelian
                    # (i.e., the order of every element is square-free).
                    is_trivial = True
                    for g in witness.generators:
                        g_ord = g.order() if callable(getattr(g, 'order', None)) else getattr(g, 'order', None)
                        if g_ord is None:
                            is_trivial = False
                            break
                        factors_g = factorint(g_ord)
                        if any(v > 1 for v in factors_g.values()):
                            is_trivial = False
                            break
                elif len(factors) == 1:
                    # A non-abelian p-group always has a non-trivial Frattini subgroup
                    is_trivial = False
                else:
                    # Fallback to computing the intersection of all maximal subgroups
                    if hasattr(witness, 'subgroups'):
                        subs = witness.subgroups()
                        proper_subs = [H for H in subs if (H.order() if callable(getattr(H, 'order', None)) else getattr(H, 'order', None)) < order]
                        if not proper_subs:
                            is_trivial = False
                        else:
                            maximal_subs = []
                            for H in proper_subs:
                                is_maximal = True
                                for K in proper_subs:
                                    h_ord = H.order() if callable(getattr(H, 'order', None)) else getattr(H, 'order', None)
                                    k_ord = K.order() if callable(getattr(K, 'order', None)) else getattr(K, 'order', None)
                                    if h_ord < k_ord:
                                        if all(g in K for g in H.generators):
                                            is_maximal = False
                                            break
                                if is_maximal:
                                    maximal_subs.append(H)
                            
                            if not maximal_subs:
                                is_trivial = False
                            else:
                                try:
                                    intersection = maximal_subs[0]
                                    for H in maximal_subs[1:]:
                                        intersection = intersection.intersection(H)
                                    int_ord = intersection.order() if callable(getattr(intersection, 'order', None)) else getattr(intersection, 'order', None)
                                    is_trivial = (int_ord == 1)
                                except Exception:
                                    common_elements = set(maximal_subs[0].elements)
                                    for H in maximal_subs[1:]:
                                        common_elements = common_elements.intersection(set(H.elements))
                                    is_trivial = (len(common_elements) == 1)
                    else:
                        raise NotImplementedError("Cannot compute Frattini subgroup for this group")
            else:
                raise ValueError("Order is None")
                
        neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: The Frattini subgroup of F is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1