import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is solvable
    try:
        solvable = witness.is_solvable
        if callable(solvable):
            solvable = solvable()
        h2 = bool(solvable)
    except Exception:
        h2 = False

    # ¬Q: G does not contain a non-trivial abelian normal subgroup
    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            try:
                order = witness.order()
            except TypeError:
                order = witness.order
                
            solvable = witness.is_solvable
            if callable(solvable):
                solvable = solvable()
                
            if order == 1:
                has_nontrivial_abelian_normal = False
            elif solvable:
                has_nontrivial_abelian_normal = True
            else:
                has_nontrivial_abelian_normal = False
                try:
                    center = witness.center()
                except TypeError:
                    center = witness.center
                    
                try:
                    center_order = center.order()
                except TypeError:
                    center_order = center.order
                    
                if center_order > 1:
                    has_nontrivial_abelian_normal = True
                else:
                    elements = witness.elements
                    if callable(elements):
                        elements = elements()
                    elements = list(elements)
                    
                    try:
                        identity = witness.identity
                    except AttributeError:
                        identity = elements[0]
                        for e in elements:
                            if getattr(e, 'is_Identity', False):
                                identity = e
                                break
                                
                    for g in elements:
                        if getattr(g, 'is_Identity', False) or g == identity:
                            continue
                        
                        conjugates = set()
                        for h in elements:
                            conj = h * g * ~h
                            conjugates.add(conj)
                            
                        conjugates = list(conjugates)
                        all_commute = True
                        for i in range(len(conjugates)):
                            for j in range(i + 1, len(conjugates)):
                                if conjugates[i] * conjugates[j] != conjugates[j] * conjugates[i]:
                                    all_commute = False
                                    break
                            if not all_commute:
                                break
                        
                        if all_commute:
                            has_nontrivial_abelian_normal = True
                            break
            
            neg_q = not has_nontrivial_abelian_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is solvable",
    "¬Q: G does not contain a non-trivial abelian normal subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2