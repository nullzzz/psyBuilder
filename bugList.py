# %%%%%%%%%%%%%%  Bugs       %%%%%%%%%%%%%%%%%%
# 1) 设备中的设备名称如果在使用后被修改，貌似其余使用的地方获得的device name还是先前的，能不能设备名已修改，相应的各个widget对应的device name 也修改呢

# 2）一个bug哈，在text中，有两个地方都有Back Color,一个在general 一个在frame中，可能是这个原因在通过Func.getProperties(cWidget.widget_id)取得的properties中只有一个 Back color 的特征值

# 3）刚才确认了下刚才的bug的确存在：bug2：如果是load出先前保存的，对于widget的一些信息，如screen name 的信息，通过 Func.getProperties(cWidget.widget_id)出来的变成了默认值 （而非修改过的设备名称），尽管手动点开后再图形界面中是正确的 (也就是联动触发问题)

# 4）先前已经解决的问题由出现了：（text widget中，直接输入的文字，在打开熟悉后general tab  会被清空）

# 5）所有widget， transparent默认值设为0%，也就是完全不透明

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



# TODOLIST
text widget --> frame-->Geometry--> X position, Y position 默认值均应为50%
text widget --> general: 'Alignment X' 可选值为 'center','left','right','wrapat','justifytomax'  注意大小写,其余的除开变量引用外，只能输入数值 （不能为负数，可以是小数），不过propertieis里面的返回还是以字符串的形式返回哈

text widget --> general: 'Alignment Y' 可选值为 'center'注意大小写,其余的除开变量引用外，只能输入数值（不能为负数，可以是小数），不过propertieis里面的返回还是以字符串的形式返回哈

# 1)
	# 1）添加一个del快捷键删除structure 和Timeline中的widgets
	# 2）修改：attributes界面的"Name"修改为 "Sort"

# 2) sound 里面增加  sound name：

# 3）output device里面也需要增加一个widgettype，sound
"""
2) Text Display:

a: General界面加一个underline选项；

: Gerneral Table:

d:	Aligment X:'center','right','centerblock','left','justifytomax' or  a number
e:	Aligment Y:'center',or a number

	#替换word wrap为：Wrapat chars: {'None'},or a number 80
f:	flipHorizontal:{'False'}
g:	flipVertical:{'True'}

h:	Style:{'normal_0'},'bold_2','italic_4','underline_8', 'outline_16', 'condense_32','extend_64' OR a number between 0-64

	Screen Name: Default ('screen.0');
	"""

# Frame:

   # + Frame Fill Color: (FrameBK Color:)
   # + Transparant: (0%)


# Image：- General:Back Color 去除

# Silder：








""""
所有duration:

选项中增加一个范围选项
默认：
0~200



Cycle：

	1）去掉order里面的Offset选项

	2）No repeat After: （待定）
	3) 直接excel复制粘贴有点问题（windows 下）
	4）导入导出问题；
"""

# Sound:


# Pan control:待定

"""
image:

	1) rotate 默认为0
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


# 8）另外在上面的工具栏中，增加一个下拉菜单显示所有对象的一个list，这样也可以通过这里来选择对象


# 9）另外，text中，在选中字框的时候需要有一个右键，有删除，前移后移动，属性的选项（属性里面有位置，字体等信息），另外工具栏中关于text的部分需要增加一个背景色的功能


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





































