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
> none
