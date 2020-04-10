# widget_id是什么
> widget_id用来唯一标识widget, 引用机制则是通过不同的widget_id指向同一个widget

# 如何新增widget
> 1. 继承lib.TabItemWidget/TabItemMainWindow类，并完成对应模块
> 2. 在Info中增加改类别new_widget_type = widget_type_name
> 3. 在Kernel的WidgetTypeCount和WidgetNameCount均新增Info.new_widget_type: 0
> 4. 在app/main.py中导入相应类，并修改Psy类的的createWidget函数
> 5. 如果有特殊的信号需要增加，修改Psy类的linkWidgetSignals函数
> 6. 在images/widgets中放入图标，格式为png
> 7. 在app/center/timeline/icon_bar.py中修改__init__函数，新增图标

# widget的引用
> 引用就是将不同的widget id指向同一个widget达到一种引用的效果
> 1. Timeline不能直接引用, 但可以通过引用cycle间接引用
> 2. 引用需要有相同的属性环境, 即父节点存在相同的cycle（引用的cycle也算相同）
> 3. 在timeline中修改名称后, 是断开引用，但是由于cycle可以引用，会牵扯到父节点作为引用，子节点的一些问题

# 信号的处理
> Psy主类中包括了创建widget及连接信号的函数, 因此所有widget的信号都被连接到Psy类中的函数handleXXXX, 但是要注意格式要求  
> 详见signals.md  

# 框架的安排
> 按照布局共分为六块  
> ## Center
>> 为tab控件, 主要是多个模块的使用
> ## Attributes
>> 用来展示
> ## Properties
>> 用来展示
> ## Structure
>> 用来展示结构信息
> ## Output
>> 用来输出消息,通过Func.print函数
> ## Menubar
>> menubar所涉及的功能和函数

# 软件的恢复与加载
> 恢复
>> 即将Info中的数据、各个源widget、structure中的结构保存在psy文件中
> 加载
>> 重新启动后, 从psy文件中读取数据

# 软件是如何重新启动的
> 实现保存了初始状态的文件init.ini（即在软件初次启动的瞬间的所有变量环境）, 在清空所有数据后（调用clear函数）, 读取该初始状态文件即可,   
> 这个初始状态是不带Timeline_0的, 需要调用initInitialTimeline来初始化Timeline  
> 因此在作出某些数据初始时的数据修改时, 我们需要重新保存初始状态, 将现有的文件手动删除后, 程序会自动保存

# 环境配置
> PyQt5: 5.14.2 or later.
> Python: 3.8 or later.
> upgrade them on time!
> 详见Requirement.txt, 务必保证PyQt5为5.14.2及以上, 否则会出现段错误


# Advice for compile
+ separate logic form UI
> This means no dialog. Just display your information in the output window by certain function.
+ less is more
> simplify unnecessary steps: such as the validation of file name, we do it in the UI part.
> more code file instead of only one. Besides, maintain a compile_func.py like func.py. we are simplifying func.py
> ...
