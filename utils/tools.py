import numpy as np
from copy import deepcopy



def union_mask(expert_masks):
    """
    get a list of separate annotations and return their union.

    """    
    temp_np = np.array(expert_masks)
    temp_sum = np.sum(temp_np, axis=0)
    binary_temp = deepcopy(temp_sum)
    binary_temp[binary_temp!=0] = 1
    binary_temp = binary_temp.astype('uint8')
    
    return binary_temp

def overlap_majority(expert_masks):
    """
    get a list of separate annoatatoins and return their overlap

    """
    n_masks = len(expert_masks)
    temp_np = np.array(expert_masks)
    temp_sum = np.sum(temp_np, axis=0)
    half_thr = int(np.ceil(n_masks/2))
    binary_temp = deepcopy(temp_sum)
    binary_temp[binary_temp<half_thr] = 0
    binary_temp[binary_temp>=half_thr] = 1    
    binary_temp = binary_temp.astype('uint8')
    
    return binary_temp