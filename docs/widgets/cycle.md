# Cycle

## frame
> 继承lib.TabItemMainWindow  
> 包含：顶部Toolbar，主空间CycleTable和Properties设置页面

## signal
> itemAdded (parent_widget_id:str, widget_id:str, widget_name:str, index:int)
>> 当新增timeline, 发送cycle的widget_id, 新增timeline的widget_id, widget_name和新增的索引（默认最后一个）
>
> itemDeleted (origin_widget:int, widget_id:str)
>> 当删除timeline，发送信号源变量Info.CycleSignal方便区分何处删除，要删除的timeline的widget_id

## shortcut 
> none

## api
> rowCount(self) -> int
>> 返回table共有多少行
>
> columnCount(self) -> int
>> 返回table共有多少列
>
> getTimelines(self) -> list
>> 按顺序进行返回所有设置的timeline  
>> 格式为 [ [timeline_name, timeline_widget_id], [], ... ]  
>> 如果某行为空则改行对应的数据为[ '', '']
>
> getAttributes(self, row: int) -> dict
>> 按行索引返回该行的数据的一个字典  
>> 格式为{ attribute_name : attribute_value }  
>> 如果属性值未填写则为 ''  
>
> getAttributeValues(self, col: int) -> list
>> 通过输入的列索引，返回该列对应的attribute的所有value的一个列表
>
> getOrder(self) -> str
>> 得到设置界面中order的值
>
> getNoRepeatAfter(self) -> str
>> 如上类推
>
> getOrderBy
>> 如上类推