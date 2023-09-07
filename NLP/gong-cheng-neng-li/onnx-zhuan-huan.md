# onnx转换

## bert-serving转onnx
```shell
bert-serving-server 1.10.0
bert-serving-client 1.10.0

# 模型文件：
chinese_L-12_H-768_A-12【tensorflow版】
```

### client调用方式
```python
from bert_serving.client import BertClient
bert_model = BertClient()
reps = bert_model.encode(["牙齿矫正","牙齿矫正","牙周炎"], show_tokens=True) #show_tokens可是展现分词结果
print(reps.shape)
print(reps[0][:5])
```

### 转ONNX
```python
"""
需要注意的源码位置：
- server.graph.optimize_graph: 读取模型的重要环节，后面读的文件位置也是启动server时拿到的保存路径。
- server.__init__:488行是读取模型构建估计器的代码；553行是构建分词器的代码，571行 convert_lst_to_features 是得到分词结果的代码。
"""
import tensorflow as tf
with tf.gfile.GFile("/var/folders/pn/py_l4tpysby/T/tmphd7kz64p",'ph') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

for n in graph_def.node:
    print(n.name)   # 可以预估一下输入节点和输出节点。bert_serving的源码里也有写明。

input_names = ['input_ids:0', 'input_mask:0', 'input_type_ids:0' ]

# b_inputs = [tf.TensorSpec([None,None], tf.int32, name= 'input_ids'), 
#             tf.TensorSpec([None, None], tf.int32, name='input_mask'),
#             tf.TensorSpec([None, None], tf.int32, name='input_type_ids')]

# 告知输入的大小
b_inputs = {'input_ids:0': [None,None],
            'input_mask:0': [None, None],
            'input_type_ids:0': [None, None]}

import tf2onnx
model_proto,_ = tf2onnx.convert.from_graph_def(graph_def, 
                                               input_names=input_names, 
                                               output_names=['final_encodes:0'],
                                               opset=12,
                                               outputpath='bert_model.onnx', 
                                               shape_override=b_inputs)
output_names = [n.name for n in model_proto.graph.output]
print(output_names)
```

### 验证结果一致性

根据第一步打印的输入，复制一份token
```python
import onnxruntime as rt
providers = ['CPUExecutionProvider']
m = rt.InferenceSession('bert_model.onnx', providers=providers)

# max_seq_length=25 源码convert_lst_to_features中补全到了最大
t_inputs = {'input_ids': [[101, 4280, 7976, 4763, 3633, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                          [101, 4280, 1453, 4142, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            'inut_mask': [[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                          [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            'input_type_ids': [[0]*25, [0]*25]}

onnx_pred = m.run(None,{"input_ids:0": t_inputs['input_ids'],
                        "input_mask:0": t_inputs['input_mask'],
                        "input_type_ids:0": t_inputs['input_type_ids']})[0]
print(onnx_pred[0][:5])
```


## pb转onnx

```shell
tensorflow 1.13.0

# 模型文件:
- model_selected
    - model.pb
    - variables
      - variables.data-00000-of-00001
      - variables.index
```

### 调用方式

```python
import tensorflow as tf
import numpy as np

example = {
    "diagnose": np.random.random(size=(3, 768)).astype(np.float32),
    "receipt": np.random.random(size=(3, 768)).astype(np.float32),
    "dia2cate": [np.array([1.0])] * 3
}

msess = tf.Session()
tf.saved_model.loader.load(msess, [tf.saved_model.tag_constants.TRAINING], './model_selected')

for n in msess.graph_def.node:
    print(n.name) # 大胆猜一下输入

"""
调用方式1
"""
diagnose_info = msess.graph.get_operation_by_name('inputs/diagnose').outputs[0] #[<tf.Tensor 'inputs/diagnose:0' shape=(?, 768) dtype=float32>]
# print(type(msess.graph.get_operation_by_name('inputs/diagnose')) # <class 'tensorflow.python.frameworks.ops.Operation>
receipt_info = msess.graph.get_operation_by_name('inputs/receipt').outputs[0]
dia2category = msess.graph.get_operation_by_name('inputs/dia2category').outputs[0]
keep_prob = msess.graph.get_operation_by_name("inputs/keep_prob").outputs[0]

receipt_pred = msess.graph.get_operation_by_name('Softmax').outputs[0] # 类别概率值
# receipt_pred = msess.graph.get_operation_by_name('pred/receipt_pred').outputs[0]  # 类别值

feed_dict = {'diagnose_info': example["diagnose"], 
             'receipt_info': example['receipt'],
             'dia2category': example['dia2cate'],
             'keep_prob': 1}

receipt_pred = msess.run(receipt_pred, feed_dict=feed_dict)
print(receipt_pred)
print("predict1 success------------")

"""
调用方式2
"""
feed_dict = {'inputs/diagnose:0': example["diagnose"], 
             'inputs/receipt:0': example['receipt'],
             'inputs/dia2category:0': example['dia2cate'],
             'inputs/keep_prob:0': 1}

receipt_pred = msess.run("Softmax:0", feed_dict=feed_dict)
print(receipt_pred)
print("predict2 success------------")

```

### 转ONNX

```python
tmp_g = tf.get_default_graph().as_graph_def()
print(tmp_g == msess.graph_def) # True
# print(len(tmp_g.node)) # 1874

# Step1：精简node，把跟计算无关的节点移除
dtype = tf.int32
print(dtype.as_datatype_enum) # 3
dtype = tf.float32  # 下面传参数需要用到
print(dtype.as_datatype_enum) # 1

print("optimize...")
from tensorflow.python.tools.optimize_for_inference import optimize_for_inference
tmp_g = optimize_for_inference(
    tmp_g,
    ['inputs/diagnose', 'inputs/receipt', 'inputs/dia2category', 'inputs/keep_prob'],
    ['Softmax'],
    [1] * 4,    # 对应 4个输入的数据类型
    False
)
print(len(tmp_g.node)) # 120

# Step2: GraphDef不支持保存Variable，但可以保存constant，通过tf.constant把weight直接存储在NodeDef中
print("freeze...")
from tensorflow.graph_util import convert_variables_to_constants
tmp_g = convert_variables_to_constants(msess, tmp_g, ['Softmax'])

# 上述两步骤，可以在 bert-serving-server 的源码中学到

# 转ONNX
import tf2onnx
input_names = ['inputs/diagnose:0', 
               'inputs/receipt:0', 
               'inputs/dia2category:0', 
               'inputs/keep_prob:0']
b_inputs = {
    'inputs/diagnose:0': [None, 768], 
    'inputs/receipt:0': [None, 768], 
    'inputs/dia2category:0': [None, 1], 
    'inputs/keep_prob:0': [1]
}

model_proto, _ = tf2onnx.convert.from_graph_def(tmp_g, 
                                               input_names=input_names, 
                                               output_names=['Softmax:0'],
                                               opset=12,
                                               outputpath='ai_model.onnx', 
                                               shape_override=b_inputs)
output_names = [n.name for n in model_proto.graph.output]
print(output_names)
print("ONNX SUCCESS")

```

### 验证结果一致性

根据第一步打印的输入，复制一份token
```python
import onnxruntime as rt
providers = ['CPUExecutionProvider']
m = rt.InferenceSession('ai_model.onnx', providers=providers)

onnx_pred = m.run(None,{"inputs/diagnose:0": example['diagnose'],
                        "inputs/receipt:0": example['receipt'],
                        "inputs/dia2category:0": example['dia2cate'],
                        "inputs/keep_prob:0": np.array([1]).astype(np.float32)})[0]
print(onnx_pred)
```



