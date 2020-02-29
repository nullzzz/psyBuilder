# Base Widget
# 包含TabItemWidget/TabItemMainWindow

## frame
> 

## signal
> propertiesChanged (widget_id:str)
>> 当widget的properties发生变化时或者想要在窗口中显示时, 发送widget_id
>
> tabClosed (widget_id:str)
>> 当widget需要关闭时, 发送widget_id
>
> waitStart (none)
>> 加载等待窗口
>
> waitEnd (none)
>> 结束等待窗口


## func need to complete
> see TabItemWidget/TabItemMainWindow

## shortcut 
> none

## api
> getProperties(none) -> dict
>> 返回widget的properties