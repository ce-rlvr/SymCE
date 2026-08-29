import sympy
from sympy.combinatorics import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, PermutationGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math

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

def extract_G_d_r(witness):
    if isinstance(witness, (tuple, list)):
        if len(witness) >= 3:
            return witness[0], witness[1], witness[2]
        elif len(witness) == 2:
            return witness[0], witness[1], None
    return witness, None, None

def get_actual_d(G):
    order = G.order()
    if order == 1:
        return 0
    factors = factorint(order)
    if len(factors) != 1:
        raise ValueError("Not a p-group")
    p = list(factors.keys())[0]
    
    D = G.derived_subgroup()
    gens_G = G.generators
    p_th_powers = [g**p for g in gens_G]
    
    gens = list(D.generators) + p_th_powers
    gens = [g for g in gens if not g.is_Identity]
    if not gens:
        Phi = PermutationGroup([G.identity])
    else:
        Phi = PermutationGroup(gens)
        
    order_quotient = order // Phi.order()
    return int(round(math.log(order_quotient, p)))

def conditions(witness) -> list[bool]:
    G, d_wit, r_wit = extract_G_d_r(witness)
    
    def check_h1():
        try:
            order = G.order()
            if order == 1:
                return True
            if order < 1:
                return False
            factors = factorint(order)
            return len(factors) == 1
        except Exception:
            return False

    def check_h2():
        try:
            if d_wit is None:
                return hasattr(G, "order")
            else:
                actual_d = get_actual_d(G)
                return d_wit == actual_d
        except Exception:
            return False

    def check_neg_q():
        try:
            actual_d = get_actual_d(G)
            
            if actual_d == 0:
                actual_r = 0
            elif actual_d == 1:
                actual_r = 1
            else:
                # For d >= 2, the Golod-Shafarevich inequality r > d^2 / 4 is always strictly true 
                # for any finite p-group. Thus, the negated conclusion (r <= d^2 / 4) is always False.
                return False
                
            if d_wit is not None and d_wit != actual_d:
                return False
            if r_wit is not None and r_wit != actual_r:
                return False
                
            return actual_r <= (actual_d ** 2) / 4
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: d is the minimal number of generators of G",
    "¬Q: r <= d^2 / 4"
]

N_HYP = 2
NEG_Q_INDEX = 2