import matplotlib.pyplot as plt

class SEAPlotter:
    """
    Responsible only for plotting SEA results.
    """

    def __init__(self):
        pass

    def plot_sea(self, time_axis, speed, density, symh, bz, output="SEA_output.eps"):
        """
        Plot 4-panel SEA result.
        """
        fig, axs = plt.subplots(4, 1, figsize=(22, 18))

        axs[0].plot(time_axis, speed, color='black')
        axs[0].set_ylabel("Speed (km/s)")
        axs[0].grid(True)

        axs[1].plot(time_axis, density, color='black')
        axs[1].set_ylabel("Density (cm⁻³)")
        axs[1].grid(True)

        axs[2].plot(time_axis, symh, color='black')
        axs[2].set_ylabel("SYM-H")
        axs[2].grid(True)

        axs[3].plot(time_axis, bz, color='black')
        axs[3].set_ylabel("Bz (nT)")
        axs[3].grid(True)

        plt.savefig(output)
        plt.show()


