# triton服务部署

https://github.com/triton-inference-server/server

https://github.com/triton-inference-server/client



## 部署

https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/performance_tuning.html

```shell
tritonserver --model-repository=/mnt/models
```



## 配置文件说明

[配置文件官方说明文档](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_configuration.html)

models下文件目录结构
- 1
	- model.onnx
- config.pbtxt


config.pbtxt 示例如下：
```shell
name: "server_name"    # 随便给服务起个名字
platform: "onnxruntime_onnx"   # 部署onnx模型
max_batch_size: 64
version_policy: {all:{}}     # 定义部署哪几个模型

# 入参结构定义，要和onnx中定义的内容保持一致
input [
		{
			name: "input"
			data_type: TYPE_INT64
			dims: [-1]
		},
		{
			name: "seq_len"
			data_type: TYPE_INT64
			dim: [1]
			reshape: {shape:[]}
		}
]

# 输出结构定义，和onnx保持一致
output [
	{
		name: "output"
		data_type: TYPE_FP32
		dims: [768]
	}
]

# 部署配置
instance_group [
	{
		count: 4         # 相当于启动4个相同的模型，worker nums
		kind: KIND_GPU
		gpus: [0]
	}
]

```

### version_policy

[配置教程](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_configuration.html?highlight=version_policy#version-policy)

> - *All*: All versions of the model that are available in the model repository are available for inferencing. `version_policy: { all: {}}`
> - *Latest*: Only the latest ‘n’ versions of the model in the repository are available for inferencing. The latest versions of the model are the numerically greatest version numbers. `version_policy: { latest: { num_versions: 2}}`
> - *Specific*: Only the specifically listed versions of the model are available for inferencing. `version_policy: { specific: { versions: [1,3]}}`

### dims

[配置教程](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_configuration.html?highlight=version_policy#shape-tensors)

在示例中出现三种情况：

- dims为1，再reshape：输入大小为[batch_size]，首先利用dims为1，代表输入为[动态维，1]【在代码处理时确实传入[batch_size, 1]】，然后再利用reshape铺平。[⭐️官方介绍](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_configuration.html?highlight=version_policy#reshape)
- dims为-1： 输入大小为[batch_size, max_seq_len]，两维都无法确定
- dims为固定值：输出大小为[batch_size, 768], 第一维不确定，第二维是固定值



## python调用

```shell
pip install tritonclient[http]
```

```python
import tritonclient.http as httpclient     # tritonclient==2.20.0
import numpy as np

INFER_SERVER = "xxxxx.com" # tritonserver地址
client = httpclient.InferenceServerClient(INFER_SERVER)

# 查看server的相关信息
model_metadata = client.get_model_metadata(model_name='server_name', model_version='1')
model_config = client.get_model_config(model_name='server_name', model_version='1')

# 喂数据
inputs_ids = np.array([[1,2,3],[4,5,0]])
seq_len = np.array([3, 2]).reshape(-1, 1)

infer_inputs = []
infer_inputs.append(httpclient.InferInput('input', inputs_ids.shape, "INT64"))
infer_inputs[0].set_data_from_numpy(inputs_ids)
infer_inputs.append(httpclient.InferInput('seq_len', seq_len.shape, "INT64"))
infer_inputs[1].set_data_from_numpy(seq_len)

# 获取输出
infer_output = httpclient.InferRequestedOutput('output', binary_data=False)

output = client.infer('server_name', infer_inputs, model_version='1', outputs=[infer_output])

```

[查看更多使用方法](https://github.com/triton-inference-server/client/blob/main/src/python/examples)



