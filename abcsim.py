import numpy as np
from matplotlib.pyplot import plot, figure, show, xlabel, ylabel

# References
# https://medium.com/giveth/deep-dive-augmented-bonding-curves-3f1f7c1fa751

# Parameters
t = np.linspace(0, 4 * 52, 1000)  # (weeks) time
i = 1  # annual growth rate of the platform
F0 = 10000  # (EUR) amount of funding allocated in the first week of the platform
d0 = 100000  # (EUR) initial raise
theta = 0.5  # initial allocation to funding pool
p0 = 0.1  # (DAI) initial price per token
p1 = 0.15  # (DAI) post-hatch price per token
rF = 0.05  # (-) percentage fee when funding projects
rS = 0.05  # (-) percentage fee when selling tokens

# Variables
kappa = p1 / (p0 * (1 - theta))  # power in power function invariant V(R,S)
iW = (1 + i) ** (1/52) - 1  # weekly growth rate of the platform
F = F0 * (1 + iW) ** t  # (EUR) Amount of funding per week
R0 = (1 - theta) * d0  # initial reserve
S0 = d0 / p0  # initial supply of tokens
V0 = S0 ** kappa / R0  # initial value of the invariant function
Slin = np.linspace(0, 5e6, 1000)  # S linear variation of token supply
PSlin = kappa * Slin ** (kappa - 1) / V0  # (EUR) P(S) token price for linear variation of the token supply
Rlin = Slin ** kappa / V0  # (EUR) R(S) reserve for linear variation of the token supply
d = theta * d0 + np.cumsum(F * rF)  # (EUR) size of funding pool


figure("Amount of funding")
plot(t, F)
xlabel("time (weeks)")
ylabel("Funding (EUR)")

figure("Token price")
plot(Slin, PSlin)
xlabel("Token supply (number of tokens)")
ylabel("Token price (EUR)")

figure("Funding pool")
plot(t, d)
xlabel("time (weeks)")
ylabel("Funding pool (EUR)")

# figure("Reserve / Supply")
# plot(Slin, Rlin)
# xlabel("Token supply (number of tokens)")
# ylabel("Reserve (EUR)")
#
# figure("Supply / Reserve")
# plot(Rlin, Slin)
# xlabel("Reserve (EUR)")
# ylabel("Token supply (number of tokens)")
#
# figure("Reserve / Token price")
# plot(Rlin, PSlin)
# xlabel("Reserve (EUR)")
# ylabel("Token price (EUR)")

# output
show()

print("Ratio with targeted funding after 2 years: ", np.sum(F[0:500-1]) / (5000 * 2000))
print("R0: ", R0)
print("kappa: ", kappa)