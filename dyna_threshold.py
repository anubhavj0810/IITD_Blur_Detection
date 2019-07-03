import math
from sklearn.preprocessing import normalize


class cameras(object):

    def __init__(self, cid, overlapping):
        self.cid = cid
        self.threshold = [0.5, 0.5, 0.5]  # array for threshold values
        self.overlapping = overlapping
        self.crowd_array = [0,0,0]
        self.noises = [0,0,0]

    def crowd_density(self, cr_de):
        self.crowd_array[cr_de[0]] = cr_de[1]

    def noise(self, noise_value, clear):
        self.noises[noise_value[0]] = noise_value[1]

    def threshold_calc(self):
        weightage = [0.5, 0.4, 0.1]
        count = 0
        for i in self.overlapping:
            self.threshold[count] = weightage[0] * i


def L2normalisation(a):
    sum_squares = 0

    for i in a:
        sum_squares += i * i

    sum_squares = math.sqrt(sum_squares)

    for i in a:
        a = a / sum_squares

    return a


c1 = cameras(0, [1, 0.3, 0.4])
c2 = cameras(1, [0.3, 1, 0.2])
c3 = cameras(2, [0.4, 0.2, 1])

# crowd density will be calculated from a separate code.These are dummy values

crowd_density_array = [1000, 500, 700]
#crowd_density_array = L2normalisation(crowd_density_array)
crowd_density_array = normalize(crowd_density_array)

c1.crowd_density([c2.cid, crowd_density_array[c2.cid]], False)
c1.crowd_density([c3.cid, crowd_density_array[c3.cid]], False)

c2.crowd_density([c1.cid, crowd_density_array[c1.cid]], False)
c2.crowd_density([c3.cid, crowd_density_array[c1.cid]], False)

c3.crowd_density([c1.cid, crowd_density_array[c1.cid]], False)
c3.crowd_density([c2.cid, crowd_density_array[c2.cid]], False)

noise_array = [0.01, 0.03, 0.02]
noise_array = L2normalisation(noise_array)
noise_array = normalize(noise_array)

c1.noise([c2.cid, noise_array[c2.cid]], False)
c1.noise([c3.cid, noise_array[c3.cid]], False)

c2.noise([c1.cid, noise_array[c1.cid]], False)
c2.noise([c3.cid, noise_array[c3.cid]], False)

c3.noise([c1.cid, noise_array[c1.cid]], False)
c3.noise([c2.cid, noise_array[c2.cid]], False)

# x = c1.threshold
