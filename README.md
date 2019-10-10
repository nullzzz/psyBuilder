# todo list
### format of conditions' info
## if
    {
        "Condition": "",
        "Yes": "",
        "No": ""
    }
## switch
    """
    {
        "switch": ""
        "case": {
            "case 1": {},
            "case 2": {},
            ...
        }
    }
    """
+ if中"yes"获取的内容及子控件getProperties
+ switch中case同理
+ 上述部分不仅是单纯控件的信息，还有object name\ switch 中的value等
+ 综上，删除wid_widget中子控件的wid，info由condition按上述格式获取。
### 2019-6-12
* 啥也不想做
---
# 关于Info类的详细说明
 **数据目前包括**
* wid_widget: [dict] widget_id -> widget
* wid_node: [dict] widget_id -> node
* name_wid: [dict] name -> [widget_id1, .widget_id2..]
* file_name: [str] 文件名
---
# widget具有的基本属性
## signals
* propertiesChange: properties -> structure</li>
## function
* changeWidgetId(widget_id): 改变widget的widget_id, 因为引用节点删除时可能删除的是源节点
* clone(widget_id): 返回以widget_id为widget_id的widget
* getProperties(): 返回properties
* getInfo(): 导入导出用，返回比getProperties更多的信息
* restore(dict): 导入导出用
* setAttributes(list): 设置可选参数，有pro_window的控件在openPro时更新attributes，其他的在apply更新


# widget信号初始化
**由main中linkWidgetSignals(widget_id)进行连接信号**
# 关于参数调用的说明
每个控件都有若干getXXX()方法，用以获取XXX参数。 e.g.Image
- getFilename
- getIsMirrorUpAndDown
- getIsMirrorLeftAndRight
- getStretchMode
- getBackColor
- getTransparent
- getClearAfter
- getScreenName
- getXAxisCoordinates
- getYAxisCoordinates
- getWidth
- getHeight
- getBorderColor
- getBorderWidth
- getDuration
- [dict]getOutputDevice
- [dict]getInputDevice
#### if
- getCondition
- [dict]getTrueWidget~~~~~~~~
- [dict]getFalseWidget
#### switch
- getSwitch
- [list]getCase
## There's another great way.
***getPropertyByKey(key: str)***
+ 获取指定参数
### other widgets
* sound soundDisplay.py from line 265 to line 360
* text  textDisplay.py  from line 218 to line 353
* video videoDisplay.py from line 275 to line 391
## 整个结构的调用
***在compile中调用self.structure.getStructure()即可得到一颗树，树类只包含了根节点，树的节点类包括了其自身name及id，父节点和所有子节点，方便调用***
+ 可以通过树类的方法print_tree查看树的详细结构
## Cycle相关
***包含两个方法***
+ getTimelines：按顺序返回所有timeline，返回格式为\[('timeline_name','timeline_wid'),(),(), ...]，若某行未设置timeline，则为('',''),即为空
+ getAttributes(index)：index为timeline所在行，即上函数所得索引，此函数根据index查找所在行，并返回属性，格式为{"attribute_name":"attribute_value", ...}
## Attributes相关
***属性的层次***
+ 第一层timeline为0，依次递增，调用方法，Info.getAttributes(widget_id，是否需要层次信息), 格式为{"attribute_name":layer(int),...}

# 关于控制台输出
+ 函数：Func.log(text: str, error: bool, timer: bool)
+ 参数：text输出文字内容，error是否为报错信息，timer是否输出时间戳
+ 功能：输出提示信息，自动定位文件及行号
+ 示例：
  ```
  try: 
      # some code
  except Exception as e:
      Func.printInfo(e, True)
  ```

