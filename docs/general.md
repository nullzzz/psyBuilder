# widget_id是什么
> widget_id用来唯一标识widget, 引用机制则是通过不同的widget_id指向同一个widget

# 如何新增widget
> 1. 继承lib.TabItemWidget/TabItemMainWindow类，完成对应模块
> 2. 在Info中增加改类别new_widget_type = an_unique_int_value，并在WidgetType新增new_widget_type: widget_type_name
> 3. 在Kernel的WidgetTypeCount和WidgetNameCount新增Info.new_widget_type: 0
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

# 

