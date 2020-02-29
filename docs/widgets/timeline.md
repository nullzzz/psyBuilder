# Timeline

## frame
> 继承lib.TabItemWidget  
> 包含：IconBar，TimelineTable

## signal
> itemAdded (parent_widget_id:str, widget_id:str, widget_name:str, index:int)
>> 当新增item时, 发送timeline的widget_id, 新增item的widget_id, widget_name及它在timeline中的位置索引
>
>itemCopied (parent_widget_id:str, origin_widget_id:str, new_widget_id:str, new_widget_name:str, index:int)
>> 当复制item时, 发送timeline的widget_id, 被复制item的widget_id, 新增item的widget_id, widget_name及它在timeline中的位置索引
>
>itemReferenced (parent_widget_id:str, origin_widget_id:str, new_widget_id:str, index:int)
>> 当引用item时, 发送timeline的widget_id, 被引用item的widget_id, 新增item的widget_id及它在timeline中的位置索引
>
>itemMoved (origin_timeline:int, dest_timeline:int, widget_id:str, origin index:int, new index:int)
>> 当item移动时, 发送原来所在的timeline的widget_id, 被移到的timeline的widget_id, 被移动的item的widget_id, 原来的位置索引, 新的位置索引
>
>itemDeleted (origin_widget:int, widget_id:str)
>> 当item删除时, 发送信号源变量Info.TimelineSignal, 被删除的item的widget_id
>
>itemNameChanged (origin_widget:int, parent_widget_id:str, widget_id:str, widget_name:int)
>> 当item名称变化时, 发送信号源变量Info.TimelineSignal, timeline的widget_id, 被修改的item的widget_id和新的widget_name
>
>itemClicked (widget_id:str)
>> 当item被点击时, 发送item的widget_id
>
>itemDoubleClicked (widget_id:str)
>> 当item被双击时, 发送item的widget_id

## shortcut 
> backspace/delete
>> 当选中某个item时, 可以快速进行删除

## api
> none
