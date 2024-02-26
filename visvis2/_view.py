import numpy as np
import pygfx as gfx

# NOTE: the implementation of viewports in pygfx can change, so we may need to adjust this code. API should stay the same tho!



class View:
    """A view to a scene.

    A View represents a view onto a scene, rendered to a rectangular
    sub-region of a canvas. You may also know this as an axes or subplot
    (Matlab, Matplotlib, Vispy, Visvis).

    The view class combines a viewport, camera, controller, and a scene.
    In pygfx these are loosely coupled (for flexibility and maintenance).
    This class wraps them in a small package that covers many plotting-like
    use-cases.
    """

    def __init__(self, renderer, rect):
        self._renderer = renderer
        self._rect = tuple(rect)

        self._viewport = gfx.Viewport(renderer)
        self._camera = gfx.OrthographicCamera(1, 1)
        self._controller = gfx.PanZoomController(self._camera, register_events=self._viewport)
        self._scene = gfx.Scene()
        self._renderer.add_event_handler(self._layout, "resize")
        self._layout()


    @property
    def rect(self):
        """ The rect (x, y, w, h) for this view.

        Each element is a string e.g. '50% + 4px'.
        """
        return self._rect

    @property
    def renderer(self):
        """ The renderer for this view.
        """
        return self._renderer

    @property
    def camera(self):
        """ The camera to use for this view.
        """
        return self._camera

    @property
    def controller(self):
        """ The pygfx controller for this view.
        """
        # todo: make it possible to change the controller mode
        return self._controller

    @property
    def scene(self):
        """The pygfx.Scene object for this view.
        """
        return self._scene

    def _layout(self, event=None):
        rw, rh = self._renderer.logical_size
        x, y, w, h = self._rect

        self._viewport.rect = (
            rect_item_to_pixels(x, rw),
            rect_item_to_pixels(y, rh),
            max(1, rect_item_to_pixels(w, rw)),
            max(1, rect_item_to_pixels(h, rh)),
        )
        # print(self._rect, self._viewport.rect)

    def _render(self):
        self._viewport.render(self._scene, self._camera)

    def _get_positions(self, *args):
        if not args:
            raise ValueError("plot() requires at least one array.")
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, np.ndarray) and arg.ndim == 2 and arg.shape[1] == 3:
                return arg.astype(np.float32, copy=False)
            else:
                yy = np.array(arg, dtype=np.float32, copy=False).ravel()
                xx = np.arange(len(yy), dtype=np.float32)
                zz = np.zeros_like(yy)
        elif len(args) == 2:
            xx = np.array(args[0], dtype=np.float32, copy=False).ravel()
            yy = np.array(args[1], dtype=np.float32, copy=False).ravel()
            zz = np.zeros_like(xx)
            positions = np.column_stack([xx, yy, zz])
        elif len(args) == 3:
            xx = np.array(args[0], dtype=np.float32, copy=False).ravel()
            yy = np.array(args[1], dtype=np.float32, copy=False).ravel()
            zz = np.array(args[2], dtype=np.float32, copy=False).ravel()
        else:
            raise ValueError("plot() requires at most three arrays.")

        # Stack together, take care of masked arrays
        xx_yy_zz = xx, yy, zz
        if any([isinstance(d, np.ma.MaskedArray) for d in xx_yy_zz]):
            return np.ma.column_stack(xx_yy_zz)
        else:
            return np.column_stack(xx_yy_zz)

    def add_line(self, *args, thickness=2, color="#00f"):
        """ Add a line object to the scene.
        """
        positions = self._get_positions(*args)

        world_object = gfx.Line(
            gfx.Geometry(positions=positions),
            gfx.LineMaterial(thickness=thickness, color=color),
        )

        self._scene.add(world_object)
        self._camera.show_object(self._scene)
        return world_object

    def add_points(self, *args, size=10, color="#00f"):
        """ Add a points object to the scene.
        """
        positions = self._get_positions(*args)
        world_object = gfx.Points(
            gfx.Geometry(positions=positions),
            gfx.PointsMaterial(size=size, color=color),
        )

        self._scene.add(world_object)
        self._camera.show_object(self._scene)
        return world_object


def rect_item_to_pixels(s, ref):
    """ Convert a css-like string representation to a number in logical pixels.
    """
    parts = s.split()
    value = 0
    cur_op = "+"
    for part in parts:
        if part == "+":
            cur_op = "+"
        elif part == "-":
            cur_op = "-"
        elif part[0].isnumeric():
            if part.endswith("px"):
                try:
                    v = float(part[:-2])
                except ValueError:
                    raise ValueError(f"Cannot interpret {repr(s)}, {repr(part[:-2])} not a float.")
            elif part.endswith("%"):
                try:
                    v = float(part[:-1])
                except ValueError:
                    raise ValueError(f"Cannot interpret {repr(s)}, {repr(part[:-1])} not a float.")
                v = (v / 100) * ref
            else:
                raise ValueError(f"Cannot interpret {repr(s)}, no unit specified for {repr(part)}.")
            if cur_op == "+":
                value += v
            elif cur_op == "-":
                value -= v
            elif not cur_op:
                raise ValueError(f"Cannot interpret {repr(s)}, no op specified before {repr(part)}.")
            else:
                raise RuntimeError("Unexpected op")  # Shouldn't happen
        else:
            raise ValueError(f"Cannot interpret {repr(s)}, don't know what {repr(part)} means.")
    return value
