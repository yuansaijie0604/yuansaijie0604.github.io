import torch
import numpy as np
import random

def set_seed(seed):
    """
    设置随机种子
    :return:
    """
    # CUDNN deterministic
    torch.backends.cudnn.deterministic = True
    # seed
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)


def pretty_duration(seconds):
    """
    时间差 %h%m%s
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)