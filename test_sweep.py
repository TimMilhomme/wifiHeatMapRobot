from sweep_fct import *
from save_fct import *


direction = 0
position_x = 0
position_y = 0
sweeper = sweep_fct('\n', ';', 'mapping', False)
saver = save_fct('\n',';','mapping',True)

sweeping = sweeper.sweepMode(position_x,position_y, direction)


saver.NewRow(*sweeping)

saver.closeFile()