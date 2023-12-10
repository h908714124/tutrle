import matplotlib.pyplot as plt
import numpy

labels = ['Waren', 'Dienstleistungen']
sizes_indien = numpy.array([453400, 308676])
sizes_deutschland=numpy.array([1657577, 406202])

def absolute_value_indien(val):
    a  = numpy.rint((val * sizes_indien.sum()) / 100)
    return '{:.0f}'.format(a)
    
def absolute_value_deutschland(val):
    a  = numpy.rint((val * sizes_deutschland.sum()) / 100)
    return '{:.0f}'.format(a)

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.set_size_inches(10, 6)
ax1.legend(title="Indien 2022")
ax2.legend(title="Deutschland 2022")
ax1.pie(sizes_indien, labels=labels, autopct=absolute_value_indien)
ax2.pie(sizes_deutschland, labels=labels, autopct=absolute_value_deutschland)
plt.savefig('exporte_indien_deutschland_2022.png')
#plt.show()


