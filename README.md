# 新功能
> [Done] 新框架中的文件的保存与恢复, 需要一个文件选择框, 类似于PyCharm.  

# bugs
> [Todo] Cycle中, 有时新增timeline时会报段错误, 升级PyQt至5.14后频次减少  
> [Done] Timeline中的拖拽位置判定不准确 => 拖动时记录item动画运动方向协同判定  
> [Done] 重新启动后, 文件选择框无法弹出 => 不再重新启动, 而是选择清空当前页面  

# bugs reported by yu
> [main.clear] 默认timeline.0未保留 => clear是清空, 新增reset是重置, 在restore的读取中, 因为有些变量就是{}, 所以不能用来判定是否读取出错  
> 您能不能把智障的启动页面去掉，或者判断一下有效的文件才显示上去，再或者不让他报错闪退ok???