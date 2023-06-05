

## loss解析


$$
log(1+\sum_{(i,j)\epsilon\Omega_{pos},(k,l)\epsilon\Omega_{neg}}{e^{\lambda(cos(u_k,u_l)-cos(u_i,u_j)}})
$$
其中$\lambda$>0是一个超参数，实验取了20

假设这样的batch数据：
```python
a = torch.tensor([0.1, 0.2, 0.8, 0.9])
label_ids = torch.tensor([0, 0, 1, 1])
```

- 由于$\lambda$取的是20，则 `a` 应该变成 $[2, 4, 16, 18]$
- 计算每个正负样本差，$[2-16,\quad2-18,\quad4-16,\quad 4-18]$
- 代入公式`torch.logsumexp(torch.tensor([0, -14, -16, -12, -14]), dim=0)`可得结果


```python
import torch  
import torch.nn as nn  
import torch.nn.functional as F  
  
# https://kexue.fm/archives/8847  
class CoSENTLoss(nn.Module):  
    def __init__(self):  
        super(CoSENTLoss, self).__init__()  
    def forward(self, reps_a, reps_b, label_ids):  
        """  
        :param reps_a: 归一化后的文本表示向量        
        :param reps_b: 归一化后的文本表示向量        
        :param label_ids: 标签[0, 1]        
        :return:  
        """        
        cosine_sim = torch.sum(reps_a * reps_b, dim=1) * 20  # lemmda 建议取 20  
        cosine_sim = cosine_sim[:, None] - cosine_sim[None, :]  
  
        labels = label_ids[:, None] < label_ids[None, :]  
        labels = labels.long()  
  
        cosine_sim = cosine_sim - (1 - labels) * 1e12  
        cosine_sim = torch.cat(  
            (torch.zeros(1).to(cosine_sim.device), cosine_sim.view(-1)), dim=0  
        )  
        loss = torch.logsumexp(cosine_sim.view(-1), dim=0)  
  
        return loss
```

上述数据为例，阶段性输出结果：
```python
cosine_sim = torch.tensor([ 2.,  4., 16., 18.])

cosine_sim = cosine_sim[:, None] - cosine_sim[None, :] # 计算每两个样本之间的差值
'''
tensor([[  0.,  -2., -14., -16.],
        [  2.,   0., -12., -14.],
        [ 14.,  12.,   0.,  -2.],
        [ 16.,  14.,   2.,   0.]])
'''

label_ids = torch.tensor([0, 0, 1, 1])

labels = label_ids[:, None] < label_ids[None, :] # 需要列入计算的位置置为True
'''
tensor([[False, False,  True,  True],
        [False, False,  True,  True],
        [False, False, False, False],
        [False, False, False, False]])
'''

cosine_sim = cosine_sim - (1 - labels) * 1e12 # 把不参与计算的位置差值设-1e12
'''
tensor([[-1.0000e+12, -1.0000e+12, -1.4000e+01, -1.6000e+01],
        [-1.0000e+12, -1.0000e+12, -1.2000e+01, -1.4000e+01],
        [-1.0000e+12, -1.0000e+12, -1.0000e+12, -1.0000e+12],
        [-1.0000e+12, -1.0000e+12, -1.0000e+12, -1.0000e+12]])
'''

cosine_sim = torch.cat(  
            (torch.zeros(1).to(cosine_sim.device), cosine_sim.view(-1)), dim=0  
        )  # 为了公式中的1，可以用e^0代替

```