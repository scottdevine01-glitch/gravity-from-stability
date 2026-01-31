import numpy as np
import matplotlib.pyplot as plt

def relic_density_constraint(M_Wp, alpha_d):
    """Relic density constraint Ωh² = 0.12."""
    return 0.12 * (0.82/alpha_d)**2 * (3.2/M_Wp)**2

def lhc_discovery_reach(M_Wp, alpha_d, L=3000):
    """HL-LHC 5σ discovery reach."""
    # Cross-section in fb
    sigma = 0.82 * (alpha_d/0.82) * (3.2/M_Wp)**2
    # Number of dilepton events
    N_ll = sigma * L * 0.01  # Br(ll) ≈ 0.01
    # Significance ~ N_ll/sqrt(N_ll + background)
    # Background ~ 1 event for m_ll > 3 TeV
    significance = N_ll / np.sqrt(N_ll + 1)
    return significance >= 5.0

# Create parameter grid
M_grid = np.linspace(2.5, 4.0, 200)  # TeV
alpha_grid = np.linspace(0.5, 1.2, 200)

M, Alpha = np.meshgrid(M_grid, alpha_grid)

# Calculate constraints
Omega = relic_density_constraint(M, Alpha)
cc_constraint = (Alpha >= 0.67) & (Alpha <= 0.97)  # α_d = 0.82 ± 0.15

# LHC discovery reach (simplified)
lhc_reachable = np.zeros_like(M)
for i in range(len(M_grid)):
    for j in range(len(alpha_grid)):
        lhc_reachable[j,i] = lhc_discovery_reach(M_grid[i], alpha_grid[j])

# Create plot
plt.figure(figsize=(10, 8))

# Plot constraints
plt.contourf(M, Alpha, Omega, levels=[0.10, 0.14], 
             alpha=0.3, colors=['orange'], label='Ωh² = 0.12±0.02')
plt.contour(M, Alpha, Omega, levels=[0.12], colors=['orange'], linewidths=2)

# Cosmological constant band
plt.fill_between(M_grid, 0.67, 0.97, alpha=0.3, color='blue',
                 label='α_d = 0.82±0.15 (Λ solution)')

# LHC discovery reach contour
plt.contour(M, Alpha, lhc_reachable, levels=[0.5], colors=['green'], 
           linewidths=2, linestyles='--', label='HL-LHC 5σ reach')

# Highlight intersection point
plt.scatter(3.2, 0.82, s=200, color='red', marker='*', 
           label='Prediction (M=3.2 TeV, α=0.82)', zorder=10)
plt.text(3.25, 0.85, 'Triple Convergence', fontsize=12, color='red')

# Formatting
plt.xlabel(r'$M_{W\prime}$ (TeV)', fontsize=14)
plt.ylabel(r'$\alpha_d = g_d^2/4\pi$', fontsize=14)
plt.title('Triple Convergence of Constraints', fontsize=16)
plt.legend(loc='upper right', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(2.5, 4.0)
plt.ylim(0.5, 1.2)

# Save figure
plt.tight_layout()
plt.savefig('triple_convergence_fig2.png', dpi=300)
plt.show()
print("Figure 2 saved as 'triple_convergence_fig2.png'")