import sympy
from sympy import S
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup for standard algebra objects
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

def compute_properties(witness):
    # 1. Check for known infinite groups (strings or SymPy sets)
    try:
        w_str = str(witness).lower().strip()
        if witness == S.Integers or w_str in ['z', 'integers', 's.integers', 'z_add', 'zz']:
            # Z under addition: abelian, no order 2, but x -> 2x is not surjective (not an automorphism)
            return True, True, False, False
        if witness == S.Reals or w_str in ['r', 'reals', 's.reals', 'r_add', 'rr']:
            # R under addition: abelian, no order 2, x -> 2x is an automorphism
            return True, True, False, True
        if witness == S.Rationals or w_str in ['q', 'rationals', 's.rationals', 'q_add', 'qq']:
            # Q under addition: abelian, no order 2, x -> 2x is an automorphism
            return True, True, False, True
        if witness == S.Complexes or w_str in ['c', 'complexes', 's.complexes', 'c_add', 'cc']:
            # C under addition: abelian, no order 2, x -> 2x is an automorphism
            return True, True, False, True
        if w_str in ['q+', 'positive_rationals', 'q_plus']:
            # Q+ under multiplication: abelian, no order 2, x -> x^2 is not surjective (not an automorphism)
            return True, True, False, False
    except Exception:
        pass

    # 2. Determine if it's a group
    is_group = False
    try:
        if hasattr(witness, 'is_group'):
            val = witness.is_group() if callable(witness.is_group) else witness.is_group
            if val is not None: is_group = bool(val)
        elif hasattr(witness, 'elements') or hasattr(witness, 'is_abelian'):
            is_group = True
    except Exception:
        pass

    # 3. Fast path for SymPy PermutationGroup
    try:
        if hasattr(witness, 'is_abelian') and hasattr(witness, 'order') and not hasattr(witness, 'relators'):
            is_ab = witness.is_abelian
            if callable(is_ab): is_ab = is_ab()
            
            order = witness.order
            if callable(order): order = order()
            
            has_2 = (order % 2 == 0)
            # For finite groups, squaring is an automorphism iff the group is abelian and has odd order
            is_auto = bool(is_ab and not has_2)
            return is_group, bool(is_ab), bool(has_2), is_auto
    except Exception:
        pass

    # 4. Fallback for custom finite groups with iterable elements
    try:
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
            is_ab = all(a*b == b*a for a in elements for b in elements)
            
            identity = next(e for e in elements if all(e*x == x for x in elements))
            has_2 = False
            for g in elements:
                if hasattr(g, 'order'):
                    if callable(g.order):
                        if g.order() == 2: has_2 = True
                    else:
                        if g.order == 2: has_2 = True
                else:
                    if g != identity and g*g == identity:
                        has_2 = True
                        
            is_hom = all((a*b)*(a*b) == (a*a)*(b*b) for a in elements for b in elements)
            squares = set(a*a for a in elements)
            is_bij = len(squares) == len(elements)
            is_auto = bool(is_hom and is_bij)
            return is_group, bool(is_ab), bool(has_2), is_auto
    except Exception:
        pass

    # 5. Duck typing for custom objects
    is_ab = True
    try:
        if hasattr(witness, 'is_abelian'):
            val = witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian
            if val is not None: is_ab = bool(val)
    except Exception:
        pass
        
    has_2 = False
    try:
        if hasattr(witness, 'has_order_2'):
            val = witness.has_order_2() if callable(witness.has_order_2) else witness.has_order_2
            if val is not None: has_2 = bool(val)
    except Exception:
        pass
        
    is_auto = False
    try:
        if hasattr(witness, 'is_squaring_automorphism'):
            val = witness.is_squaring_automorphism() if callable(witness.is_squaring_automorphism) else witness.is_squaring_automorphism
            if val is not None: is_auto = bool(val)
        elif hasattr(witness, 'is_automorphism'):
            val = witness.is_automorphism() if callable(witness.is_automorphism) else witness.is_automorphism
            if val is not None: is_auto = bool(val)
    except Exception:
        pass
        
    return is_group, is_ab, has_2, is_auto

def conditions(witness) -> list[bool]:
    try:
        is_group, is_ab, has_2, is_auto = compute_properties(witness)
        h1 = bool(is_group)
    except Exception:
        h1 = False
        is_ab = has_2 = is_auto = False

    try:
        # The conclusion states: f is an automorphism iff G is abelian and contains no elements of order 2
        q = (is_auto == (is_ab and not has_2))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let G be a group",
    "¬Q: The conclusion 'f is an automorphism iff G is abelian and contains no elements of order 2' is false"
]

N_HYP = 1
NEG_Q_INDEX = 1