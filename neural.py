import numpy as np
"""
    Made a Nueral Network with 1 input nodes, 0 hidden layer , output layer of 1 nodes
"""

def sigmoid(z):
    return 1/(1 + np.exp(-1*z))

no_hidden_layers = 0
total_layers = no_hidden_layers + 2
num_wts = total_layers - 1

class NeuralNetwork:
    #----------------------------------declaring wts---------------------------
    def __init__(self):
        self.wts = []
        inp_to_hl = np.random.rand(1,1)
        self.wts.append(inp_to_hl)

        #--------------------------------/declaring wts----------------------------

        #---------------------------------declaring layers-------------------------
        self.layer = []
        for i in range(total_layers):
            self.layer.append(1)
        #--------------------------------/declaring layers-------------------------

    def feed_forward(self):
            for i in range(total_layers-1):
                self.layer[i+1] = sigmoid(np.dot(self.layer[i], self.wts[i]))

    def choice(self):
        if self.layer[-1][0] > 0.5: return 1
        else: return 0
        
obj = NeuralNetwork()
obj.layer[0] = np.array([-2])
obj.feed_forward()
print(obj.choice())
print(obj.wts)