from data import *
from figure import *
from utility import *

# ================================================================

setting_dir="../examples/non-uniform/"

lower_bound=0.001 # lower bound of volume fraction

# ================================================================

file=setting_dir+"CSD.csv"
tmp1=variable_read(file)
size=variable("size","um",[])
volume_fraction=variable("volume fraction","-",[])

for i in range(len(tmp1[1].value)):
    if tmp1[1].value[i] > lower_bound:
        size.value.append(tmp1[0].value[i])
        volume_fraction.value.append(tmp1[1].value[i])

output=[size,volume_fraction]
variable_output(output,file)
