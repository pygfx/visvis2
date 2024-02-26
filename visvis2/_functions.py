from wgpu.gui.auto import WgpuCanvas, run as wgpu_run
import pygfx as gfx

from ._view import View


__all__ = ["create_view", "create_views", "run"]


def create_view():
    """ Create a canvas with a single view.
    """
    views = create_views(1, 1)
    return views[0]


def create_views(nrows=1, ncols=1, *, title="pygfx canvas", size=(640, 480), max_fps=30, vsync=True):
    """Create a canvas with multiple views in a grid.
    """
    canvas = WgpuCanvas(title=title, size=size, max_fps=max_fps, vsync=vsync)
    renderer = gfx.WgpuRenderer(canvas)

    # # Background
    # viewport0 = gfx.Viewport(renderer)
    # camera0 = gfx.NDCCamera()
    # scene0 = gfx.Background(None, gfx.BackgroundMaterial("#fff"))

    views = []
    margin = 10
    for row in range(nrows):
        for col in range(ncols):
            x = f"{100*col/ncols:0.2f}% + {margin/2:0.2f}px"
            w = f"{100/ncols:0.2f}% - {margin:2f}px"
            y = f"{100*row/nrows:0.2f}% + {margin/2:0.2f}px"
            h = f"{100/nrows:0.2f}% - {margin:2f}px"
            v = View(renderer, rect=(x, y, w, h))
            views.append(v)

    views = tuple(views)

    def animate():
        for v in views:
            v._render()
        renderer.flush()

    renderer.request_draw(animate)

    return views


def run():
    wgpu_run()
