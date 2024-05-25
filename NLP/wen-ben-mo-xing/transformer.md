# transformer


- 理论：
  - [https://zhuanlan.zhihu.com/p/43493999](https://zhuanlan.zhihu.com/p/43493999)
  - [咕叽咕叽小菜鸟](https://blog.csdn.net/u010366748/article/details/111183674)
- 实现：
  - [https://tensorflow.google.cn/tutorials/text/nmt_with_attention](https://tensorflow.google.cn/tutorials/text/nmt_with_attention)
  - [https://tensorflow.google.cn/tutorials/text/transformer](https://tensorflow.google.cn/tutorials/text/transformer)
  - [http://nlp.seas.harvard.edu/2018/04/03/attention.html](http://nlp.seas.harvard.edu/2018/04/03/attention.html)



## 细节反思

https://www.jianshu.com/p/55b4de3de410

### attention为什么scaled?

当输入信息的维度 d 比较高，点积模型的值通常有比较大方差，从而导致 softmax 函数的梯度会比较小。因此，缩放点积模型可以较好地解决这一问题。

### 相较于加性模型，点积模型具备哪些优点？

常用的Attention机制为加性模型和点积模型，理论上加性模型和点积模型的复杂度差不多，
但是点积模型在实现上可以更好地利用矩阵乘积，从而计算效率更高（实际上，随着维度d的增大，加性模型会明显好于点积模型）。

### 为什么是双线性点积模型？

双线性点积模型，引入非对称性，更具健壮性（Attention mask对角元素值不一定是最大的，也就是说当前位置对自身的注意力得分不一定最高）。

### 为什么使用多头注意力,而不是单头注意力？

《Attention Is All You Need》作者认为：平均注意力加权降低了有效的分辨率，即它不能充分体现来自不同表示子空间的信息。
而使用多头注意力机制有点类似于CNN中同一卷积层内使用多个卷积核的思想。可以增强模型对于文本在不同子空间中体现出的不同的特性，避免了平均池化对这种特性的抑制。 
