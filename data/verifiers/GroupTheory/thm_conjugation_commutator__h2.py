import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, PermutationGroup) or hasattr(witness, "elements"):
            h1 = True
            elements = list(witness.elements)
            if len(elements) > 60:
                elements = elements[:60]
                
            for x in elements:
                x_inv = x**-1
                for y in elements:
                    y_inv = y**-1
                    c1 = x_inv * y_inv * x * y
                    c2 = x * y * x_inv * y_inv
                    for z in elements:
                        z_inv = z**-1
                        
                        lhs1 = z_inv * c1 * z
                        lhs2 = z_inv * c2 * z
                        
                        zx = z_inv * x * z
                        zy = z_inv * y * z
                        rhs1 = zx**-1 * zy**-1 * zx * zy
                        rhs2 = zx * zy * zx**-1 * zy**-1
                        
                        if lhs1 != rhs1 or lhs2 != rhs2:
                            neg_q = True
                            break
                    if neg_q: break
                if neg_q: break

        elif isinstance(witness, tuple):
            if len(witness) == 4:
                G, x, y, z = witness
                if isinstance(G, PermutationGroup) or hasattr(G, "elements"):
                    try:
                        in_G = x in G and y in G and z in G
                    except Exception:
                        elements = list(G.elements)
                        in_G = x in elements and y in elements and z in elements
                    
                    if in_G:
                        h1 = True
                        x_inv = x**-1
                        y_inv = y**-1
                        z_inv = z**-1
                        
                        c1 = x_inv * y_inv * x * y
                        lhs1 = z_inv * c1 * z
                        zx = z_inv * x * z
                        zy = z_inv * y * z
                        rhs1 = zx**-1 * zy**-1 * zx * zy
                        
                        c2 = x * y * x_inv * y_inv
                        lhs2 = z_inv * c2 * z
                        rhs2 = zx * zy * zx**-1 * zy**-1
                        
                        if lhs1 != rhs1 or lhs2 != rhs2:
                            neg_q = True
                            
            elif len(witness) == 3:
                x, y, z = witness
                h1 = True
                x_inv = x**-1
                y_inv = y**-1
                z_inv = z**-1
                
                c1 = x_inv * y_inv * x * y
                lhs1 = z_inv * c1 * z
                zx = z_inv * x * z
                zy = z_inv * y * z
                rhs1 = zx**-1 * zy**-1 * zx * zy
                
                c2 = x * y * x_inv * y_inv
                lhs2 = z_inv * c2 * z
                rhs2 = zx * zy * zx**-1 * zy**-1
                
                if lhs1 != rhs1 or lhs2 != rhs2:
                    neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "not Q: conjugate of commutator is not commutator of conjugates"
]

N_HYP = 1
NEG_Q_INDEX = 1