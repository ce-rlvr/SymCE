import itertools
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        R1, R2 = witness
        R1 = list(R1)
        R2 = list(R2)
        # Verify that elements support multiplication
        if R1:
            _ = R1[0] * R1[0]
        if R2:
            _ = R2[0] * R2[0]
        h1 = True
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # Compute center of R1
            c1 = []
            for z in R1:
                if all(z * r == r * z for r in R1):
                    c1.append(z)
            
            # Compute center of R2
            c2 = []
            for z in R2:
                if all(z * r == r * z for r in R2):
                    c2.append(z)
            
            # Direct product of centers: Z(R1) x Z(R2)
            dp_centers = list(itertools.product(c1, c2))
            
            # Compute center of the direct product R1 x R2: Z(R1 x R2)
            c_dp = []
            for z1, z2 in itertools.product(R1, R2):
                is_center = True
                for r1, r2 in itertools.product(R1, R2):
                    if z1 * r1 != r1 * z1 or z2 * r2 != r2 * z2:
                        is_center = False
                        break
                if is_center:
                    c_dp.append((z1, z2))
            
            # Check if Z(R1 x R2) == Z(R1) x Z(R2)
            if len(dp_centers) != len(c_dp):
                neg_q = True
            else:
                neg_q = False
                # Check if every element in c_dp is in dp_centers
                for x_ in c_dp:
                    found = False
                    for y_ in dp_centers:
                        if x_[0] == y_[0] and x_[1] == y_[1]:
                            found = True
                            break
                    if not found:
                        neg_q = True
                        break
                
                # Check if every element in dp_centers is in c_dp
                if not neg_q:
                    for y_ in dp_centers:
                        found = False
                        for x_ in c_dp:
                            if x_[0] == y_[0] and x_[1] == y_[1]:
                                found = True
                                break
                        if not found:
                            neg_q = True
                            break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is the direct product of R1 and R2",
    "¬Q: The center of R is not equal to the direct product of the centers of R1 and R2"
]

N_HYP = 1
NEG_Q_INDEX = 1