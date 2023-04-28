
# 作用

解耦：使程序直接实现松耦合，修改一个函数，不会有串联关系。

提高处理效率：ＦＩＦＯ　＝　现进先出，ＬＩＦＯ　＝　后入先出。

队列可以并发的派多个线程，对排列的线程处理，并切每个需要处理线程只需要将请求的数据放入队列容器的内存中，线程不需要等待，当排列完毕处理完数据后，线程在准时来取数据即可。

请求数据的线程只与这个队列容器存在关系，处理数据的线程down掉不会影响到请求数据的线程，队列会派给其他线程处理这分数据，它实现了解耦，提高效率。

队列内会有一个有顺序的容器，列表与这个容器是有区别的，列表中数据虽然是排列的，但数据被取走后还会保留，而队列中这个容器的数据被取后将不会保留。当必须在多个线程之间安全地交换信息时，队列在线程编程中特别有用。

# 四种队列

## Queue：FIFO 即first in first out 先进先出

基本用法：

```python
from queue import Queue

#基本FIFO队列  先进先出 FIFO即First in First Out,先进先出
#maxsize设置队列中，数据上限，小于或等于0则不限制，容器中大于这个数则阻塞，直到队列中的数据被消掉
q = Queue(maxsize=0)

#写入队列数据
q.put(0)
q.put(1)
q.put(2)

#输出当前队列所有数据
print(q.queue)
#删除队列数据，并返回该数据
q.get()
print(q.queue)

# 输出:
# deque([0, 1, 2])
# deque([1, 2])

```

## LifoQueue：LIFO 即last in first out 后进先出

基本用法：

```python
from queue import LifoQueue
#LIFO即Last in First Out,后进先出。与栈的类似，使用也很简单,maxsize用法同上
lq = LifoQueue(maxsize=0)

# 同Queue
```

## PriorityQueue：优先队列，级别越低，越优先

基本用法：

```python
from queue import PriorityQueue
# 存储数据时可设置优先级的队列
# 优先级设置数越小等级越高
pq = PriorityQueue(maxsize=0)

#写入队列，设置优先级
pq.put((9,'a'))
pq.put((7,'c'))
pq.put((1,'d'))

#输出队例全部数据
print(pq.queue)

#取队例数据，可以看到，是按优先级取的。
pq.get()
pq.get()
print(pq.queue)#输出：[(9, 'a')]
```

## deque:双边队列

基本用法：

```python
from queue import deque
#双边队列
dq = deque(['a','b'])

#增加数据到队尾
dq.append('c')
#增加数据到队左
dq.appendleft('d')

#输出队列所有数据   deque(['d', 'a', 'b', 'c'])
print(dq)
#移除队尾，并返回   c
print(dq.pop())
#移除队左，并返回   d
print(dq.popleft())
```

**collections中也有deque的实现**

```python
from collections import deque

queue = deque([2，3，4])
# 输出队列所有数据
print(q)
#移除队尾，并返回   4
print(q.pop())
#移除队左，并返回   2
print(q.popleft())
```

# 生产消费模型

```python
from queue import Queue
#生产消费模型
qq = Queue(maxsize=10)

def product(name):
    count = 1
    while True:
        q.put('步枪{}'.format(count))
        print('{}生产步枪{}支'.format(name,count))
        count+=1
        time.sleep(0.3)

def cousume(name):
    while True:
        print('{}装备了{}'.format(name,q.get()))
        time.sleep(0.3)

        q.task_done()

#部队线程
p = threading.Thread(target=product,args=('张三',))
k = threading.Thread(target=cousume,args=('李四',))
w = threading.Thread(target=cousume,args=('王五',))

p.start()
k.start()
w.start()
```

# 参考

[https://www.cnblogs.com/yhleng/p/9493457.html](https://www.cnblogs.com/yhleng/p/9493457.html "https://www.cnblogs.com/yhleng/p/9493457.html")
