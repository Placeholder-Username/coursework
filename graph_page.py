import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DAYS_PER_WEEK

days = (["Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"])
values = ([])
for day in days:
    values.append(day)

plt.bar(days,values)
plt.show()