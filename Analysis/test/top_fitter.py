import numpy as np
from scipy.optimize import minimize

# Define some constants
m_W = 80.4  # W boson mass
m_t = 172.5  # top quark mass

# Define the chi square function
def chi2(p, met):
    p1, p2 = p
    return ((p1[0]+p2[0]-met[0])**2 + (p1[1]+p2[1]-met[1])**2)

# Define the objective function to be minimized
def objective(p, met, jets):
    p1, p2 = p
    # Compute the W boson momenta
    W1 = jets[0] + p1
    W2 = jets[1] + p2
    # Compute the top quark momenta
    t1 = W1 + jets[2]
    t2 = W2 + jets[3]
    # Compute the invariant masses of the top quarks
    m1 = np.sqrt((t1[0]**2 + t1[1]**2 + t1[2]**2) - m_t**2)
    m2 = np.sqrt((t2[0]**2 + t2[1]**2 + t2[2]**2) - m_t**2)
    # Compute the chi square
    return chi2(p, met) + ((m1-m_t)**2 + (m2-m_t)**2)/(15.**2)

# Define the observed MET and jet momenta
met = np.array([50., 30.])
jets = np.array([
    np.array([100., 20., 10.]),
    np.array([70., -10., 5.]),
    np.array([40., 60., -5.]),
    np.array([30., -70., -10.]),
])

# Use a minimization algorithm to find the minimum of the chi square function
result = minimize(objective, x0=[np.zeros(3), np.zeros(3)], args=(met, jets), method='Nelder-Mead')

# Divide the observed MET between the two neutrinos to obtain their momenta
p1, p2 = result.x
neutrino_momenta = np.array([p1, p2])
neutrino_momenta[0] += met/2.
neutrino_momenta[1] -= met/2.

# Use the reconstructed neutrino momenta along with the observed jet momenta to reconstruct the two top quarks
W1 = jets[0] + neutrino_momenta[0]
W2 = jets[1] + neutrino_momenta[1]
t1 = W1 + jets[2]
t2 = W2 + jets[3]

# Print the results
print("Neutrino momenta:")
print(neutrino_momenta)
print("Top quark momenta:")
print(t1)
print(t2)
