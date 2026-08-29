import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            I = witness['I']
            is_homogeneous = witness.get('is_homogeneous', lambda x: True)
        else:
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            I = witness.I
            is_homogeneous = getattr(witness, 'is_homogeneous', lambda x: True)
            
        elements_set = set(elements)
        I_set = set(I)
        
        def generate_ideal(gens):
            ideal = set(gens)
            ideal.add(zero)
            changed = True
            while changed:
                changed = False
                new_elements = set()
                for x in ideal:
                    for y in ideal:
                        s = add(x, y)
                        if s not in ideal:
                            new_elements.add(s)
                    for r in elements:
                        p1 = mul(x, r)
                        p2 = mul(r, x)
                        if p1 not in ideal: new_elements.add(p1)
                        if p2 not in ideal: new_elements.add(p2)
                if new_elements:
                    ideal.update(new_elements)
                    changed = True
            return ideal

        # H_1: I is a proper homogeneous ideal of R
        h1_ok = False
        if I_set.issubset(elements_set) and I_set != elements_set:
            if generate_ideal(I_set) == I_set:
                H_in_I = [x for x in I_set if is_homogeneous(x)]
                if generate_ideal(H_in_I) == I_set:
                    h1_ok = True

        # H_2: I is maximal among all proper homogeneous ideals of R
        h2_ok = False
        if h1_ok:
            h2_ok = True
            H_not_in_I = [x for x in elements if is_homogeneous(x) and x not in I_set]
            for h in H_not_in_I:
                J = generate_ideal(list(I_set) + [h])
                if J != elements_set:
                    h2_ok = False
                    break

        # ¬Q: I is not a prime ideal of R
        neg_q_ok = False
        for a in elements:
            if a in I_set: continue
            for b in elements:
                if b in I_set: continue
                if mul(a, b) in I_set:
                    neg_q_ok = True
                    break
            if neg_q_ok:
                break

        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a proper homogeneous ideal of R",
    "H_2: I is maximal among all proper homogeneous ideals of R",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2