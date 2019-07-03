import math

class cameras(object):

    def __init__(self,cid,overlapping):
        self.cid = cid
        self.threshold = [0.5,0.5,0.5] #array for threshold values
        self.overlapping = overlapping
        self.crowd_array = []
        self.noises = []

    def crowd_density(self,cr_de,clear):
        if(clear == True):
            self.crowd_array = []
        else:
            self.crowd_array.append(cr_de)

    def noise(self,noise_value,clear):
        if(clear == True):
            self.noises = []
        else:
            self.noises.append(noise_value)

    def threshold_calc(self):
        weightage = [0.5,0.4,0.1]
        count = 0
        for i in self.overlapping:
            self.threshold[count] = weightage[0]*i
            
    
def L2normalisation(a):
    sum_squares = 0

    for i in a:
        sum_squares+= i*i

    sum_squares = math.sqrt(sum_squares)
    
    for i in a:
        a = a/sum_squares

    return a
   
c1 = cameras(1,[1,0.3,0.4])#shouldn't overlapping of c1 wrt to c2 and c2 wrt c1 be the same value?
c2 = cameras(2,[0.4,1,0.5])
c3 = cameras(3,[0.2,0.6,1])

crowd_density_array = [1000,500,700]
crowd_density_array = L2normalisation(crowd_density_array)

c1.crowd_density([c2.cid,crowd_density_array[1]],False)
c1.crowd_density([c3.cid,crowd_density_array[2]],False)

c2.crowd_density([c1.cid,crowd_density_array[0]],False)
c2.crowd_density([c3.cid,crowd_density_array[2]],False)

c3.crowd_density([c1.cid,crowd_density_array[0]],False)
c3.crowd_density([c2.cid,crowd_density_array[1]],False)


noise_array = [0.01,0.03,0.02]
noise_array = L2normalisation(noise_array)

c1.noise([c2.cid,noise_array[1]],False)
c1.noise([c3.cid,noise_array[2]],False)

c2.noise([c1.cid,noise_array[0]],False)
c2.noise([c3.cid,noise_array[2]],False)

c3.noise([c1.cid,noise_array[0]],False)
c3.noise([c2.cid,noise_array[1]],False)


#x = c1.threshold
