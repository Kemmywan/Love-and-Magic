import math
import torch
from torch import nn
from torch.nn import functional as F
from d2l import torch as d2l

F.one_hot(torch.tensor([0, 2]), len(vocab))