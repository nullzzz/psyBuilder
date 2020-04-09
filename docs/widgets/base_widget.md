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
> 请一定按照要求命名重写, 方便集中调用

## shortcut 
> 可以通过设置快捷的上下文  
> shortcut.setContext(Qt.WidgetWithChildrenShortcut)  
> 来避免快捷键冲突

## api
> getProperties(none) -> dict
>> 返回widget的properties


# widget的基本情况
## refresh mechanism
+ What
> some device information such as screen, sound and so on.
+ Time
> when the icon clicked in the timeline, we call function getProperties() to display properties.
## default_properties
> each object has a default_properties, here's some function about it:
+ updateInfo()
> save the UI information to default_properties.
+ getInfo()
> return it.
+ setProperties(dict)
> update it from another dictionary, <b>attention</b>: we just change the object instead of replacing it.
+ loadSetting()
> update UI information from it.
+ getProperties()
> return properties to display, For the sake of beauty, we only show a part of properties.
# device的基本情况
## global devices
> We have a class named TianBianYiDuoYun control different types of device: Input, Output, Quest and Tracker.
> The cloud contains a parameter: simple info, which stores simple information: device id and device name.
> When we open the device window, we refresh it.
## duration devices
## detail
> Every device selection window has three parts: device bar, device home and describer.
> It also has a default_properties. When we click button ok or apply after choosing devices, we update information from describer(UI) and load them in device home.
+ device bar
> you know it.
+ device home
> Inherit from itemList. It controls all devices we selected.
+ describer
> Inherit from stackWidget. It is used to display and modify parameters. 
> One to one correspondence between device and describer.
