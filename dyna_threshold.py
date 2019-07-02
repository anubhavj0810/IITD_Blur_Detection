
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
    
c1 = cameras(1,[1,0.3,0.4])
c2 = cameras(2,[0.4,1,0.5])
c3 = cameras(2,[0.2,0.6,1])


c1.crowd_density([c2.cid,0.5],False)
c1.crowd_density([c3.cid,0.3],False)

#x = c1.threshold