# Base Widget
# 包含TabItemWidget/TabItemMainWindow

## frame
> none

## signal
> propertiesChanged (widget_id:int)
>> 当widget的properties发生变化时或者想要在窗口中显示时, 发送widget_id
>
> waitStart (none)
>> 加载等待窗口
>
> waitEnd (none)
>> 结束等待窗口

## shortcut 
> none

## api
> getProperties(none) -> dict
>> 返回widget的properties