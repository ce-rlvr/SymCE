import itertools
import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: f: R \\to S is a ring homomorphism",
    "H_2: Nil(R) and Nil(S) denote the nilradicals of R and S, respectively",
    "¬Q: f(Nil(R)) \\not\\subseteq Nil(S)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # H_1: f is a ring homomorphism from R to S
        h1 = True
        for a in witness.R:
            if witness.f(a) not in witness.S:
                h1 = False
                break
        if h1:
            for a in witness.R:
                for b in witness.R:
                    if witness.f(witness.add_R(a, b)) != witness.add_S(witness.f(a), witness.f(b)):
                        h1 = False
                        break
                    if witness.f(witness.mul_R(a, b)) != witness.mul_S(witness.f(a), witness.f(b)):
                        h1 = False
                        break
                if not h1: break
        if h1:
            if witness.f(witness.one_R) != witness.one_S:
                h1 = False
    except Exception:
        h1 = False

    try:
        # H_2: Nil(R) and Nil(S) are the nilradicals (prime radicals) of R and S
        def is_nilradical(elements, add, mul, zero, I):
            # Check if I is a subset containing zero
            for x in I:
                if x not in elements: return False
            if zero not in I: return False
            
            # Check if I is a two-sided ideal
            for a in I:
                for b in I:
                    if add(a, b) not in I: return False
            for a in I:
                for r in elements:
                    if mul(a, r) not in I: return False
                    if mul(r, a) not in I: return False
                    
            def multiply_ideals(A, B):
                prods = []
                for a in A:
                    for b in B:
                        p = mul(a, b)
                        if p not in prods:
                            prods.append(p)
                added = True
                while added:
                    added = False
                    n = len(prods)
                    for i in range(n):
                        for j in range(n):
                            s = add(prods[i], prods[j])
                            if s not in prods:
                                prods.append(s)
                                added = True
                return prods

            power = []
            for x in I:
                if x not in power:
                    power.append(x)
                    
            # Check if I is nilpotent
            is_nil = False
            for _ in range(len(elements) + 1):
                if all(x == zero for x in power):
                    is_nil = True
                    break
                power = multiply_ideals(power, I)
            if not is_nil:
                return False
            
            # Check if I is the largest nilpotent ideal
            # (i.e., no element outside I generates a nilpotent ideal)
            for x in elements:
                if x in I: continue
                gen = []
                for r in elements:
                    for s in elements:
                        p = mul(r, mul(x, s))
                        if p not in gen:
                            gen.append(p)
                added = True
                while added:
                    added = False
                    n = len(gen)
                    for i in range(n):
                        for j in range(n):
                            s = add(gen[i], gen[j])
                            if s not in gen:
                                gen.append(s)
                                added = True
                
                power_gen = list(gen)
                is_nil_gen = False
                for _ in range(len(elements) + 1):
                    if all(y == zero for y in power_gen):
                        is_nil_gen = True
                        break
                    power_gen = multiply_ideals(power_gen, gen)
                if is_nil_gen:
                    return False
            return True

        h2 = is_nilradical(witness.R, witness.add_R, witness.mul_R, witness.zero_R, witness.Nil_R) and \
             is_nilradical(witness.S, witness.add_S, witness.mul_S, witness.zero_S, witness.Nil_S)
    except Exception:
        h2 = False

    try:
        # ¬Q: f(Nil(R)) is NOT a subset of Nil(S)
        neg_q = False
        for x in witness.Nil_R:
            if witness.f(x) not in witness.Nil_S:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]