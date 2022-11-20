import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

plt.style.use('bmh')


def mixed_line_widths():
    lines = np.cumsum(np.random.uniform(low=0, high=10, size=(30, 100)), axis=1)

    avg_line = np.mean(lines, axis=0)

    plt.figure(figsize=(15, 8))

    for line in lines:
        plt.plot(line, linewidth=5, alpha=0.1, color='b', linestyle='-')

    plt.plot(avg_line, linewidth=5, alpha=1, color='black', linestyle='-')
    plt.plot(avg_line, linewidth=2, alpha=1, color='r', linestyle='-')

    plt.title('Mixing lines widths to make a line more emphasized')


def colourmaps():
    from matplotlib import cm

    x = np.arange(100)
    y1 = np.cumsum(np.random.random(100))
    y2 = np.cumsum(np.random.random(100))

    colourmap = cm.get_cmap('inferno', 100)
    colours1 = [colourmap(i) for i in x]

    top = cm.get_cmap('Oranges_r', 100)  # r means reversed version
    bottom = cm.get_cmap('Blues', 100)  # combine it all
    newcolors = np.vstack((top(np.linspace(0, 1, 100)),
                           bottom(np.linspace(0, 1, 100))))  # create a new colormaps with a name of OrangeBlue
    orange_blue = ListedColormap(newcolors, name='OrangeBlue')
    colours2 = [orange_blue(i) for i in x]

    plt.figure(figsize=(15, 8))
    plt.scatter(x, y1, c=colours1)
    plt.scatter(x, y2, c=colours2)

    plt.title('Different colourmaps')


def line_coloured_by_its_gradient():
    from matplotlib import cm
    colourmap = cm.get_cmap('RdBu', 256)

    line = np.sin(np.linspace(0, 6.28, 100))

    line_grad = np.gradient(line)
    line_grad_norm = line_grad/np.max(np.abs(line_grad))
    grad_index = (line_grad_norm*128).astype(int)+127

    plt.figure(figsize=(15, 8))
    plt.plot(line, linewidth=4, color='black', linestyle=':')
    for i, (y1, y2) in enumerate(zip(line[:-1], line[1:])):
        plt.plot([i, i+1], [y1, y2], alpha=1, color=colourmap(grad_index[i]), linestyle='-')

    plt.title('The color of this line is changing according to the gradient')


if __name__ == "__main__":
    mixed_line_widths()
    colourmaps()
    line_coloured_by_its_gradient()

    plt.show()
