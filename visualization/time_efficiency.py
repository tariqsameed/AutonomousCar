# import pandas
import pandas as pd
import seaborn as sns
import numpy
from datetime import datetime


print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

data = pd.read_csv("time_comparison.csv")
print(data)

bplot = sns.boxplot(y='Time in Minutes', x='Prototype',
                 data=data,
                 width=0.5,
                 palette="colorblind")

# add swarmplot
bplot=sns.swarmplot(y='Time in Minutes', x='Prototype',
              data=data,
              color='black',
              alpha=0.75)


# save as jpeg
bplot.figure.savefig("time_efficiency",
                    format='jpeg',
                    dpi=100)


print(data['Time in Minutes'])


q1_x = numpy.percentile(data['Time in Minutes'], 25)
q3_x = numpy.percentile(data['Time in Minutes'], 75)
print(q1_x)
print(q3_x)