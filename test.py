import numpy as np
import visvis2 as vv

v1, v2 = vv.create_views(2, 1)

line1 = v1.add_line([1,2,3, 1, 9, 2, 8, 3])

line2 = v2.add_points(5*np.sin(np.linspace(0, 10, 60)), color='red')

vv.run()


##

# Similar code for fastplotlib
#
# import fastplotlib as flp
# import numpy as np
#
# p = flp.Plot()
#
# xy = np.array(np.column_stack([range(8), [1,2,3, 1, 9, 2, 8, 3]]))
# line = p.add_line(xy.astype(np.float32))
# print("line is", repr(line))
# p.show()