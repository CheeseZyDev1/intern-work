#Simulated GraphLearner for the interns to practice building a GUI with.
import copy
import random

class graph_learner:
  def __init__(self,h=5,gen_mode='max'):
    self.h = h #Currently serves no purpose but can be adapted to serve as an h_max, the maximum h allowed during generation
    self.gen_mode = gen_mode
    self.history = []

  def set_gen_mode(self,gen_mode):
    #Sets the text generation mode
    self.gen_mode = gen_mode

  def add_data(self,doc,h=5):
    self.history.extend(doc)

  def gen_next_n(self,promp,n,h=5):
    #Given an input sequence promp and n return promp + n new words as object prompt.
    #Iteratively calls gen_next() n times.
    prompt = copy.deepcopy(promp) #Makes a deep copy so we don't change the original input..
    for x in range(n):
      prompt = self.gen_next(prompt,h)
    return prompt

  def gen_next(self,promp,h=5):
    prompt = copy.deepcopy(promp)
    n = random.choice(self.history)
    prompt.append(n)
    return prompt