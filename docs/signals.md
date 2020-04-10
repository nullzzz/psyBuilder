# 信号的连接
> dock widgets
>> 在app.main中__init__函数中调用了initDockWidgets, 初始化各个dock widgets并连接简单信号  
>
> widgets
>> 在app.main中有linkWidgetSignals函数, 用来连接widget的信号, 主要在createWidget函数中调用
>

# 信号的规则
> handleItemAdded(parent_widget_id: str, widget_id: str, widget_name: str, index: int = -1):
>> 在parent_widget_id所指的widget中创建了一个为输入参数的widget_id和widget_name的widget, 其在structure中显示的次序为index
>
> handleItemCopied(parent_widget_id: str, origin_widget_id: str, new_widget_id: str, new_widget_name: str, index: int):
>> 在parent_widget_id所指的widget中复制了origin_widget_id所指的widget,  
>> 生成了为输入参数的new_widget_id和new_widget_name的widget, 其在structure中显示的次序为index
>
> handleItemReferenced(parent_widget_id: str, origin_widget_id: str, new_widget_id: str, index: int):
>> 在parent_widget_id所指的widget中引用了origin_widget_id所指的widget,  
>> 生成了为输入参数的new_widget_id和引用widget的widget_name的widget, 其在structure中显示的次序为index
> 
> handleItemMoved(origin_parent_widget_id: str, dest_parent_widget_id: str, widget_id: str, origin_index: int, dest_index: int):
>> widget_id所指的widget从origin_parent_widget_id所指的widget中移动到dest_origin_widget_id所指的widget中, 
>> origin_index和dest_index是指他们的显示的次序
> 
> handleItemDeleted(sender_widget: int, widget_id: str):
>> 删除widget_id所指的widget，包括删除structure中的节点和关闭tab(如果打开的话且无引用)
>> sender主要用来判断从何处发出删除指令: 包括timeline, cycle, structure.
>
> handleItemNameChanged(sender_widget: int, widget_id: str, new_widget_name: str):
>> 当widget_id所指的widget的widget_name发生改变时, 改变其在timeline或者structure中的name, 并且修改tab的名称
>> sender主要用来判断从何处发出删除指令: 包括timeline, structure(cycle中不能修改，只能增删).
>
> handleItemClicked(widget_id: str):
>> 当timeline的item被单击时, 显示widget_id所指的widget的attributes和properties
>
> handleItemDoubleClicked(widget_id: str):
>> 当timeline的item或者structure中的节点被点击时, 打开对于tab, 显示attributes和properties
>
> handlePropertiesChanged(widget_id: str):
>> 当widget_id所指的widget的properties的被修改时, 更新properties窗口显示
>
> handleCurrentTabChanged(widget_id: str):
>> 当前的tab发生变化时, 更新attributes和properties窗口显示
>
> handleTabClosed(widget_id: str):
>> 关闭widget_id所指的widget的tab
