import math

import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)

precision = 4


def get_q(degree, constant_index):
    res = ""
    for i in reversed(range(1, degree)):
        res += f'C_{constant_index}t^{i} + '
        constant_index = constant_index + 1
    res += f'C_{constant_index}'
    constant_index = constant_index + 1
    return res.replace('^1', ''), constant_index


def is_zero(a):
    return abs(a) < 10 ** (-precision)


latex_str = ""


def show_latex(str):
    plt.text(0, 1, str)
    plt.axis('off')
    plt.show()


n = int(input()) + 1
coefs = input().strip().split()
if n != len(coefs):
    print("Not enough or too many coefs")
    exit(1)
print("Coefs:", coefs)
coefs = np.array(coefs, dtype=complex)
x = np.roots(coefs)
print("Roots:", x)

x, d = np.unique(x.round(precision), return_counts=True)
m = len(x)
print("Roots number:", m)
print("Unique roots:", x)
print("D:", d)
c_index = 1
answer = ""
for l in range(0, m):
    nu = np.imag(x[l])
    lambda_ = np.real(x[l])
    if not is_zero(math.cos(nu)):
        q, c_index = get_q(d[l], c_index)
        if is_zero(math.cos(nu) - 1.):
            answer += f'({q}) + '
        else:
            answer += f'({q})\cos({nu}t) + '
    if not is_zero(math.sin(nu)):
        q, c_index = get_q(d[l], c_index)
        if is_zero(math.sin(nu) - 1.):
            answer += f'({q}) + '
        else:
            answer += f'({q})\sin({nu}t) + '
latex_str += "$" + answer.replace('[', '{').replace(']', '}').strip('+() ').replace(' + -', ' - ') + "$"
show_latex(latex_str)
