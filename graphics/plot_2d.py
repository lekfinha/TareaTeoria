
def plot_2d(x, y, title="2D Plot", xlabel="X-axis", ylabel="Y-axis"):
    """
    Function to create a 2D plot using matplotlib.

    Parameters:
    x (list): X-axis data.
    y (list): Y-axis data.
    title (str): Title of the plot.
    xlabel (str): Label for the X-axis.
    ylabel (str): Label for the Y-axis.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    # guardamos la grafica
    plt.savefig(f"graphics/{title}.png")
    plt.show()