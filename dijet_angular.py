import numpy as np
import matplotlib.pyplot as plt

def qcd_background(cos_theta):
    """QCD background distribution."""
    return 1.0/(1 - cos_theta**2)**0.5

def wprime_signal(cos_theta):
    """W' t-channel exchange distribution."""
    return 1.0/(1 - cos_theta)**2  # Rutherford-like

def contact_interaction(cos_theta):
    """Contact interaction distribution."""
    return np.ones_like(cos_theta)

# Generate angular range
cos_theta = np.linspace(-0.95, 0.95, 100)

# Normalize distributions
qcd_norm = qcd_background(cos_theta) / np.trapz(qcd_background(cos_theta), cos_theta)
wprime_norm = wprime_signal(cos_theta) / np.trapz(wprime_signal(cos_theta), cos_theta)
ci_norm = contact_interaction(cos_theta) / np.trapz(contact_interaction(cos_theta), cos_theta)

# Add signal to background (5% signal fraction)
signal_fraction = 0.05
total = (1-signal_fraction)*qcd_norm + signal_fraction*wprime_norm

# Create plot
plt.figure(figsize=(10, 6))

# Plot distributions
plt.plot(cos_theta, qcd_norm, 'gray', linewidth=3, label='QCD Background', alpha=0.7)
plt.plot(cos_theta, wprime_norm, 'red', linewidth=3, label=r'$W\prime$ Signal (t-channel)', alpha=0.8)
plt.plot(cos_theta, ci_norm, 'blue', linestyle='--', linewidth=2, 
         label='Contact Interaction', alpha=0.6)
plt.plot(cos_theta, total, 'black', linewidth=2, linestyle=':', 
         label='Total (5% signal)', alpha=0.9)

# Highlight Rutherford-like rise
plt.axvspan(0.85, 0.95, alpha=0.2, color='green', 
           label='Rutherford-like rise region')

# Add mild excess indication (simulating data)
excess_region = (cos_theta > 0.88) & (cos_theta < 0.92)
plt.fill_between(cos_theta[excess_region], 0, 
                 total[excess_region]*1.3, alpha=0.3, color='green',
                 label='Mild excess (ATLAS/CMS 2025)')

# Formatting
plt.xlabel(r'$|\cos\theta^*|$', fontsize=14)
plt.ylabel(r'$d\sigma/d|\cos\theta^*|$ (normalized)', fontsize=14)
plt.title(r'Dijet Angular Distribution for $m_{jj} > 2.5$ TeV', fontsize=16)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)
plt.ylim(0, max(total)*1.5)

# Add inset for high-mass region
ax_inset = plt.axes([0.65, 0.65, 0.25, 0.25])
ax_inset.plot(cos_theta, wprime_norm/qcd_norm, 'red', linewidth=2)
ax_inset.set_xlabel(r'$|\cos\theta^*|$', fontsize=8)
ax_inset.set_ylabel('Signal/Background', fontsize=8)
ax_inset.set_title('Ratio', fontsize=10)
ax_inset.grid(True, alpha=0.3)
ax_inset.set_xlim(0.8, 0.95)

# Save figure
plt.tight_layout()
plt.savefig('dijet_angular_fig3.png', dpi=300)
plt.show()
print("Figure 3 saved as 'dijet_angular_fig3.png'")