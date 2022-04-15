import os.path
import argparse

from pyaxidraw import axidraw
from rich.console import Console

parser = argparse.ArgumentParser(description='Plot an SVG')
parser.add_argument('--path', type=str, default="svg/bunny.svg", help='Path to the svg file to plot.', dest='file', nargs=1)
parser.add_argument('--preview', type=str, default=None, const="preview.svg", help='Path to preview output.', dest='preview', nargs="?")
parser.add_argument('--optimize', type=bool, default=False, const=True, help='Whether to optimize the plot.', dest='optimize', nargs="?")
parser.add_argument('--config', type=str, default=None, help='Path to the Axidraw config file to use.', dest='config', nargs=1)
args = parser.parse_args()

console = Console()

def plot(path_to_svg, optimize, preview):
    if not os.path.exists(path_to_svg):
        console.print("File {0} does not exist; exiting.".format(path_to_svg))
        exit()

    console.print("Calculating plot time for file {0}...".format(path_to_svg))

    ad = axidraw.AxiDraw()
    ad.plot_setup(path_to_svg)
    ad.options.preview  = True
    output_svg = ad.plot_run(True)

    total = ad.pt_estimate // 1000
    minutes = int(total / 60)
    secs = int(total % 60)

    console.print("Estimated plot time: {0} minutes {1} seconds.".format(minutes, secs))

    if optimize:
        ad.plot_setup(path_to_svg)
        ad.options.reordering = 2
        ad.options.preview = True
        output_svg = ad.plot_run(True)

        total = ad.pt_estimate // 1000
        minutes = int(total / 60)
        secs = int(total % 60)

        console.print("Optimized plot time: {0} minutes {1} seconds".format(minutes, secs))

    if preview:
        console.print("Saving preview to {0}".format(preview))
        file = open(preview, 'w')
        file.write(output_svg)
        file.close()
        exit()

    console.print("Continue to plot?")
    res = input("y/n: ")

    if res != "y":
        console.print("Exiting.")
        exit()

    console.print("Starting plot...")
    ad.options.preview  = False
    ad.plot_run()
    console.print("Plot finished. Exiting.")


if __name__ == "__main__":
    plot(args.file, args.optimize, args.preview)
