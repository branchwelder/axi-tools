import yaml
import click
from svg.path import parse_path
from rich import print


class Axi:
    def __init__(self):
        self.connected = False
        self.ad = None
        self.workspace = None
        self.config = None

    def import_workspace(self, path):
        with open(path, "r") as file:
            self.workspace = yaml.safe_load(file)
        self.workspace_path = path

    def import_config(self, path):
        with open(path, "r") as file:
            self.config = yaml.safe_load(file)
        self.config_path = path
        self.ad.options.pen_pos_up = self.config["pen_pos_up"]
        self.ad.units = self.config["units"]
        self.ad.update()

    def current_workspace(self):
        print(self.workspace)

    def current_options(self):
        print(self.config)

    def connect(self):
        from pyaxidraw import axidraw  # import module

        self.ad = axidraw.AxiDraw()  # Initialize class
        self.ad.interactive()  # Enter interactive context
        assert self.ad.connect() == True

    def disconnect(self):
        self.ad.moveto(0, 0)
        self.ad.disconnect()

    def wet_brush(self):
        water = self.workspace["water"]
        self.ad.moveto(water["x"], water["y"])
        self.ad.pendown()
        self.ad.penup()
        self.ad.pendown()
        self.ad.penup()

    def set_location(self, locationID):
        loc = self.workspace["locations"][locationID]
        self.ad.moveto(loc["x"], loc["y"])
        inc = 0.1

        while True:
            click.echo(
                "calibrate (y to accept, wasd to move, zxc to change increment): "
            )
            c = click.getchar()
            if c == "y":
                break
            if c == "w":
                self.ad.move(0, -inc)
            if c == "a":
                self.ad.move(-inc, 0)
            if c == "s":
                self.ad.move(0, inc)
            if c == "d":
                self.ad.move(inc, 0)
            if c == "z":
                inc = 0.1
                click.echo(f"Increment:{inc}")
            if c == "x":
                inc = 0.5
                click.echo(f"Increment:{inc}")
            if c == "c":
                inc = 1
                click.echo(f"Increment:{inc}")

        curr = self.ad.current_pos()
        self.workspace["locations"][locationID]["x"] = curr[0]
        self.workspace["locations"][locationID]["y"] = curr[1]

    def set_z(self, locationID):
        loc = self.workspace["locations"][locationID]
        self.ad.moveto(loc["x"], loc["y"])
        self.ad.options.pen_pos_down = loc["z"]
        self.ad.pendown()
        current = self.ad.options.pen_pos_down
        inc = 1
        while True:
            click.echo(f"Current height: {current}")
            click.echo("ws to raise/lower, y to accept, zxc to change increment")
            c = click.getchar()
            if c == "y":
                break
            if c == "w":
                current += inc
            if c == "s":
                current -= inc
            if c == "z":
                inc = 1
            if c == "x":
                inc = 5
            if c == "z":
                inc = 10

            self.ad.options.pen_pos_down = current
            self.ad.update()
            self.ad.penup()
            self.ad.pendown()
        self.workspace["locations"][locationID]["z"] = current
        self.ad.penup()

    def save_workspace(self):
        with open(self.workspace_path, mode="wt", encoding="utf-8") as file:
            yaml.dump(self.workspace, file)

    def save_config(self):
        with open(self.config_path, mode="wt", encoding="utf-8") as file:
            yaml.dump(self.config, file)

    def draw_parsed_path(self, path):
        p = parse_path(path)
        for segment in p:
            command = type(segment).__name__
            print(command)
            if command == "Line":
                print(segment)
                # print(segment.start.real, segment.start.imag)
                # print(segment.end.real, segment.end.imag)
                # self.ad.lineto(segment.end.real, segment.end.imag)
            elif command == "Close":
                print(segment)
            elif command == "CubicBezier":
                print(segment)
            elif command == "Move":
                print(segment)
                # self.ad.moveto(segment.end.real, segment.end.imag)

    def parse_path_template(self, path):
        # p = path.format(r=r, d=2 * r)

        # print(parse_path(path))
        pass

    def pick_up_paint(self, color, path, r):
        loc = self.workspace["locations"][color]
        p = path.format(r=r, d=2 * r)
        self.ad.moveto(loc["x"], loc["y"])
        self.draw_parsed_path(parse_path(p))


paint_pickup_path = "m -{r} -{r} l{d} 0 0 {d} -{d} 0 z"
hourglass = "l 1 1 l -1 0 l 1 -1 Z"
asdf = """M213.1,6.7c-32.4-14.4-73.7,0-88.1,30.6C110.6,4.9,67.5-9.5,36.9,6.7C2.8,22.9-13.4,62.4,13.5,110.9
  C33.3,145.1,67.5,170.3,125,217c59.3-46.7,93.5-71.9,111.5-106.1C263.4,64.2,247.2,22.9,213.1,6.7z"""

if __name__ == "__main__":
    a = Axi()
    a.connect()
    a.import_workspace("workspace.yaml")
    a.import_config("config.yaml")
    # a.current_workspace()
    # a.current_options()
    # a.set_location("black")
    # a.set_z("black")
    # a.pick_up_paint("black", paint_pickup_path, 0.25)
    a.draw_parsed_path(asdf)
    a.save_workspace()
    a.save_config()
    a.disconnect()
