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
