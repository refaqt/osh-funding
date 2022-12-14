import numpy as np
from matplotlib.pyplot import plot, figure, show, xlabel, ylabel

# References
# https://medium.com/giveth/deep-dive-augmented-bonding-curves-3f1f7c1fa751

# Parameters
N = 4 * 52 + 1  # number of weeks
t = np.linspace(0, N - 1, N)  # (weeks) time
i = 0.5  # annual growth rate of the platform
F0 = 10000  # (EUR) amount of funding allocated in the first week of the platform (week 0)
d0 = 100000  # (EUR) initial raise
theta = 0.5  # initial allocation to funding pool
p0 = 0.1  # (DAI) initial price per token
p1 = 0.3  # (DAI) post-hatch price per token
rF = 0.05  # (-) percentage fee when funding projects
rS = 0.05  # (-) percentage fee when selling tokens
rT = 0.1  # (-) percentage of funding that is used to create tokens for the donor

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
d = theta * d0 + np.cumsum(F * rF)  # (EUR) size of Refaqt's funding pool

# Simulation
Fp = np.cumsum(F * (1 - rF) * (1 - rT))  # Total amount of funding to projects
S_m = np.zeros((N, N))  # Number of tokens, split up per week
DeltaS = np.zeros((N, N))  # Change of the supply each week
R_m = np.zeros((N, N))  # Part of the reserve attributed to the tokens minted each week
DeltaR = np.zeros((N, N))  # Change of the reserve each week
S = np.zeros(N)
S[0] = S0
R = np.zeros(N)
R[0] = R0
P = np.zeros(N)
P[0] = p1
j = 0

for i in range(1, N):
    DeltaR[i, i] = F[i-1] * (1 - rF) * rT
    # Insert change in reserve from burning of tokens here
    R[i] = R[i-1] + np.sum(DeltaR[i, :])
    DeltaS[i, i] = (V0 * R[i]) ** (1 / kappa) - S[i-1]
    S[i] = S[i-1] + np.sum(DeltaS[i, i])
    P[i] = kappa * R[i] ** ((kappa - 1) / kappa) / V0 ** (1 / kappa)

pROI = [F[i] / DeltaS[i, i] for i in range(1, N)]  # (EUR) token price at which donations in this week would be earned back
mROI = pROI / P[1:]  # (-) required multiple to reach ROI

figure("Weekly amount of funding")
plot(t, F)
xlabel("time (weeks)")
ylabel("Funding / week (EUR)")

figure("Token price")
plot(Slin, PSlin)
xlabel("Token supply (number of tokens)")
ylabel("Token price (EUR)")

figure("Funding pool Refaqt")
plot(t, d)
xlabel("time (weeks)")
ylabel("Funding (EUR)")

figure("Projected yearly revenue Refaqt")
plot(t, F * rF * 52)
xlabel("time (weeks)")
ylabel("Revenue (EUR)")

figure("DeltaS")
plot(t, [DeltaS[i, i] for i in range(len(F))])
xlabel("time (weeks)")
ylabel("\Delta S (-)")

figure("DeltaR")
plot(t, [DeltaR[i, i] for i in range(len(F))])
xlabel("time (weeks)")
ylabel("\Delta R (-)")

figure("Reserve / weekly")
plot(t, R)
xlabel("time (weeks)")
ylabel("Reserve (EUR)")

figure("Supply / weekly")
plot(t, S)
xlabel("time (weeks)")
ylabel("Supply (-)")

figure("Cumulative funding to projects")
plot(t, Fp)
xlabel("time (weeks)")
ylabel("Funding (EUR)")

figure("Token price / weekly")
plot(t, P)
xlabel("time (weeks)")
ylabel("Token price (EUR)")

figure("Price at which there will be ROI")
plot(t[1:], pROI)
xlabel("time (weeks)")
ylabel("pROI (EUR)")

figure("Multiple required to reach ROI")
plot(t[1:], mROI)
xlabel("time (weeks)")
ylabel("mROI (-)")

# figure("Reserve / Supply")
# plot(Slin, Rlin)
# xlabel("Token supply (number of tokens)")
# ylabel("Reserve (EUR)")
#
figure("Supply / Reserve")
plot(Rlin, Slin)
xlabel("Reserve (EUR)")
ylabel("Token supply (number of tokens)")
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