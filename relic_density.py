import numpy as np
import matplotlib.pyplot as plt

def freeze_out_temperature(M_Wp, alpha_d):
    """Calculate freeze-out temperature x_f = M/T_f."""
    g = 3  # SU(2) triplet
    g_star = 106.75
    M_Pl = 1.22e19  # GeV
    
    # Annihilation cross-section (in GeV^-2)
    sigma_v = (np.pi * alpha_d**2) / (M_Wp**2)
    
    # Solve freeze-out equation iteratively
    x_f = 20  # Initial guess
    for _ in range(10):
        x_f = np.log(0.038 * g * M_Pl * M_Wp * sigma_v * x_f**0.5 / np.sqrt(g_star))
    
    return x_f

def relic_density(M_Wp, alpha_d):
    """Calculate relic density Ωh²."""
    x_f = freeze_out_temperature(M_Wp, alpha_d)
    return 1.07e9 * x_f / (np.sqrt(106.75) * 1.22e19)

# Parameter space
M_range = np.linspace(2.0, 5.0, 100)  # TeV
alpha_range = np.linspace(0.5, 1.5, 100)

M_grid, Alpha_grid = np.meshgrid(M_range, alpha_range)
Omega_grid = np.zeros_like(M_grid)

# Calculate relic density grid
for i in range(len(M_range)):
    for j in range(len(alpha_range)):
        Omega_grid[j,i] = relic_density(M_range[i], alpha_range[j])

# WIMP miracle line: Ωh² = 0.12
from scipy.interpolate import griddata

# Find contour where Ωh² = 0.12
contour_levels = [0.10, 0.12, 0.14]

# Create plot
plt.figure(figsize=(12, 10))

# Contour plot
CS = plt.contour(M_grid, Alpha_grid, Omega_grid, levels=contour_levels,
                 colors=['orange', 'red', 'orange'], linewidths=[2, 3, 2])
plt.clabel(CS, inline=True, fontsize=10, fmt='Ωh² = %.2f')

# Fill between contours
plt.contourf(M_grid, Alpha_grid, Omega_grid, levels=[0.10, 0.14], 
             alpha=0.2, colors=['orange'])

# Mark our prediction
plt.scatter(3.2, 0.82, s=300, color='red', marker='*', 
           label=r'Prediction: $M=3.2$ TeV, $\alpha=0.82$', zorder=10)
plt.text(3.25, 0.85, 'WIMP Miracle', fontsize=12, color='red')

# Plot thermal cross-section line
sigma_thermal = 1e-9  # 1 pb in GeV^-2
alpha_thermal = np.sqrt(sigma_thermal * M_range**2 / np.pi)
plt.plot(M_range, alpha_thermal, 'blue', linestyle='--', linewidth=2,
        label=r'$\langle\sigma v\rangle = 1$ pb (thermal)')

# Highlight allowed region
allowed = (Omega_grid >= 0.10) & (Omega_grid <= 0.14)
M_allowed = M_grid[allowed]
Alpha_allowed = Alpha_grid[allowed]
if len(M_allowed) > 0:
    plt.scatter(M_allowed, Alpha_allowed, s=1, color='green', alpha=0.1,
               label='Ωh² = 0.12±0.02')

# Formatting
plt.xlabel(r'$M_{W\prime}$ (TeV)', fontsize=14)
plt.ylabel(r'$\alpha_d = g_d^2/4\pi$', fontsize=14)
plt.title('Dark Matter Relic Density', fontsize=16)
plt.legend(loc='upper right', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(2.0, 5.0)
plt.ylim(0.5, 1.5)

# Add text box with calculation details
textstr = '\n'.join([
    r'$\Omega h^2 \approx \frac{1.07\times 10^9}{M_{\mathrm{Pl}}}\frac{x_f}{\sqrt{g_*}}$',
    r'$x_f \approx \ln\left[0.038\frac{g M_{\mathrm{Pl}} M \langle\sigma v\rangle}{\sqrt{g_*}}\right]$',
    r'$\langle\sigma v\rangle \approx \frac{\pi\alpha_d^2}{M^2}$',
    '',
    f'For M=3.2 TeV, α=0.82:',
    f'  x_f ≈ {freeze_out_temperature(3.2, 0.82):.1f}',
    f'  Ωh² ≈ {relic_density(3.2, 0.82):.3f}'
])

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('relic_density_calculation.png', dpi=300)
plt.show()
print("Relic density figure saved as 'relic_density_calculation.png'")

# Print specific prediction
print(f"\nRelic density prediction for our parameters:")
print(f"  M_W' = 3.2 TeV")
print(f"  α_d = 0.82")
print(f"  Freeze-out parameter: x_f = {freeze_out_temperature(3.2, 0.82):.1f}")
print(f"  Ωh² = {relic_density(3.2, 0.82):.3f}")
print(f"  Planck measurement: Ωh² = 0.120 ± 0.001")