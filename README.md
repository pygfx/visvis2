# visvis2

An easy and fun plotting API for pygfx.


## Purpose

Pygfx is pretty powerful and flexible, but it's API is somewhat verbose
for doing explorative visualization. This is intentional, because
designing a (high-level) API comes with many subtle choices.

In `visvis2` we provide a minimal API to setup a pygfx visualization.
Other libs may do the same, but with different API's. Like e.g. fastplotlib!


## Vision

The idea of visvis2 is to be a thin API layer over pygfx. It's so thin
you can still see pygfx. It provides an easy API to create subplots (we
call them "views"), and position them. It has methods to add content
to the scene. These methods auto-convert input data (e.g. convert lists
to numpy arrays) for convenience. But they simply return pygfx objects.

No dependencies except pygfx itself.

For now this lib does not create its own world object classes or
shaders. I.e. all is vanilla pygfx.


## Status

Very much experimental. Was triggerd by my old prof asking for viz tools
for medical visualization. Not sure if I'll push this much further.
Fastplotlib may be equally suited with some added suppoer for e.g.
volumes.

For now it's a nice toy to get a feel for what's needed from pygfx to
make a lib *like this* work. E.g. axes, grids, ticks, legends ...

And it can serve as an example for others how have plans for creating
a library on top of pygfx.



## About the name

[Visvis](https://github.com/almarklein/visvis) is a Python visualization
library that I started during my PhD. It actually still works, but is
sub-optimal in many ways. After various detours it feels like with pygfx
I'm finishing what I started with visvis. This lib (visvis2) brings it full
circle by providing the easy API too.

Visvis2 is not compatible with visvis in any way.
