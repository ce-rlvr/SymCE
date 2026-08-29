import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def DirectSum(*args):
    return ("DirectSum", args)

def DirectProduct(*args):
    return ("DirectProduct", args)

def SafeFreeGroup(*args, **kwargs):
    if sympy.oo in args or sympy.oo in kwargs.values():
        return "FreeGroup_oo"
    try:
        from sympy.combinatorics.free_groups import FreeGroup as SympyFreeGroup
        return SympyFreeGroup(*args, **kwargs)
    except Exception:
        return "FreeGroup_oo"

FreeGroup = SafeFreeGroup

def get_order(G):
    try:
        if callable(G.order):
            return G.order()
        else:
            return G.order
    except Exception:
        return sympy.oo

def is_finite_group(H):
    try:
        if hasattr(H, 'order'):
            ord_H = get_order(H)
            return ord_H < sympy.oo
        if isinstance(H, PermutationGroup):
            return True
        return False
    except Exception:
        return False

def has_nontrivial_hom(A, H):
    try:
        from sympy.combinatorics.homomorphisms import homomorphism
        gens = A.generators
        id_H = None
        for e in H.elements:
            if getattr(e, 'is_Identity', False):
                id_H = e
                break
        if id_H is None:
            if hasattr(H, 'identity'):
                id_H = H.identity
            else:
                id_H = list(H.elements)[0]
                
        count = 0
        for images in itertools.product(H.elements, repeat=len(gens)):
            if count > 1000:
                return sympy.gcd(get_order(A), get_order(H)) > 1
            count += 1
            if all(img == id_H for img in images):
                continue
            try:
                h = homomorphism(A, H, gens, images, check=True)
                if h:
                    return True
            except ValueError:
                pass
        return False
    except Exception:
        return sympy.gcd(get_order(A), get_order(H)) > 1

def is_infinite_hom(G, H):
    if not is_finite_group(H):
        return False
        
    ord_H = get_order(H)
    if ord_H == 1:
        return False

    if isinstance(G, str):
        if G == "FreeGroup_oo":
            return ord_H > 1
        if "infty" in G.lower() or "oo" in G.lower() or "infinity" in G.lower() or "..." in G:
            n = None
            s = G.lower()
            idx = s.find('z')
            if idx != -1:
                sub = s[idx+1:]
                if sub.startswith('_'):
                    sub = sub[1:]
                digits = ""
                for char in sub:
                    if char.isdigit():
                        digits += char
                    else:
                        break
                if digits:
                    n = int(digits)
            if n is not None:
                return sympy.gcd(n, ord_H) > 1
            return ord_H > 1

    if isinstance(G, tuple):
        if G and G[0] in ("DirectSum", "DirectProduct"):
            args = G[1]
            is_inf = False
            for arg in args:
                if arg == sympy.oo or (isinstance(arg, str) and ("..." in arg or "infty" in arg.lower() or "oo" in arg.lower())):
                    is_inf = True
                    break
            if is_inf:
                base_groups = [arg for arg in args if not (arg == sympy.oo or isinstance(arg, str))]
                if not base_groups:
                    return ord_H > 1
                for bg in base_groups:
                    if hasattr(bg, 'generators') and hasattr(H, 'generators'):
                        if has_nontrivial_hom(bg, H):
                            return True
                    else:
                        if ord_H > 1:
                            return True
                return False

    if hasattr(G, 'func') and G.func.__name__ == 'Product':
        try:
            limits = G.args[1:]
            if any(limit[-1] == sympy.oo for limit in limits):
                return ord_H > 1
        except Exception:
            pass

    try:
        from sympy.polys.rings import PolyRing
        if isinstance(G, PolyRing) and G.domain == sympy.ZZ:
            return ord_H > 1
    except Exception:
        pass

    return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = is_finite_group(H)
    except Exception:
        h1_ok = False

    try:
        neg_q = is_infinite_hom(G, H)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "¬Q: The set of all group homomorphisms from G to H is infinite"
]

N_HYP = 1
NEG_Q_INDEX = 1