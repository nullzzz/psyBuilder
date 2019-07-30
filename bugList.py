# %%%%%%%%%%%%%%  Bugs  %%%%%%%%%%%%%%%%%%
#
#
# 3）整体关于引用时候预览的问题：如果某个特征是引用的话，预览的时候不好处理，我们这么解决，如果该属性是引用，则预览的时候直接调用该属性的默认值（仅限预览的时候哈）
#
#
#
#
# # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# 所有控件中涉及的File Name用相对路径（图片，声音等），即相对于程序保存目录的路径
#
# Sound:
# 	Gernral:
# 		4) Volume control 下面的volume，可以输入的范围是-1 - 1，既可以是1个数字(num1)，也可以是两个数字（中间逗号，num1,num2）

#
# Eyetracker：
#
# 		3) eye tracker 下所有的（除开open）widget下面增加一个eyeTrackerName（widgetName）
#
#
# QUEST：
# 	QUESTUpdate中增加一个下拉菜单，QuestName: 从多个可能的 Quest中选择
#
# 	block掉QUESTGETVALUE得widget


# TODOLIST

# 1)
# 1）添加一个del快捷键删除structure 和Timeline中的widgets





# Silder：








""""



Cycle：

	1）去掉order里面的Offset选项

	2）No repeat After: （待定）
	3) 直接excel复制粘贴有点问题（windows 下）
	4）导入导出问题；
"""


# slide：
#
# 0）slider 属性框里面增加 + frame table （内容同单独的image 里面的frame）
# 1）Basic Flowchart 名称修改为 Basic Geometry
#
# 2）下面三个合并为一个 polygon，在polygon里面的gemetry里面可以自定义顶点（默认3个，添加一个增加和一个减少按钮，最少需要有3个顶点，最多20个），默认添加后的图形是正N边形状
#
# conditional:
# process:
# input/output:

# 3）在cycle里面增加两个参数，也就是start 和end angle：（默认分别是0,360）,0 度对应是正上垂直线（+Y）。另外需要注意的默认是在不是全圆的扇形中，缺口的边框没有（也就是只有弧线）。
# 当然fill color的时候还是需要填充出一个扇形的。

# 4）另外在特征中，增加一个选项来决定是否呈现缺口的边框。


# 5）另外是线条的时候选中貌似很困难，优化一下

# 6）另外，最好是选中后增加一个快捷键，按del 删除

# 7）另外能否增加一个功能，鼠标按着拖拽一个区域，自动选中区域中所有，以进行删除


# 8）另外在上面的工具栏中，增加一个下拉菜单显示所有对象的一个list，这样也可以通过这里来选择对象。右边加一个属性按钮，点击该按钮弹出属性


# 9）另外，text中，在选中字框的时候需要有一个右键，有删除，前移后移动，属性的选项（属性里面有位置，字体等信息），另外工具栏中关于text的部分需要增加一个背景色的功能

# 10)text 需要有属性框，具体参照于鹏
#
# 11）text编辑状态下，在其它地方点击鼠标应该退出编辑状态
#
# 12）所有widget选中右键，菜单，del，bring front，bring back，properties



# 9）另外，在工具栏中，增加一个小属性按钮用于选中某一个子widget的时候，点他弹出来属性选项（同现在其他的双击效果一样）
#


# 10）右边框中的Backgrouds 修改为stimuli


	# 在视频，图片的general里面，去掉，Screen Name，和Clear after选项，因为sider作为一个整体有这两个选项

# 11）另外一个小bug，貌似 text总是在最上面

# 返回参数中对于slide中每一个widget都需有一个参数来表示他们的层级（也就是在前面和后面的问题），或者向现在timeline返回一样，返回的一个widgetlist里面前面就是在最下面的widget，后面的就是在最上面的widget
#

# 直线里面不需要Center X Y的选项，直接由 P1和P2计算得到；

# 12) slide 中，slider property 里面增加Frame table，内容同image widget


# Switch：Case 下所有wdiget的名称只允许有字母数字和下划线（且数字不能在前面）





































