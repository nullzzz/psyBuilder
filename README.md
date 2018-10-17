<p><big>命名规范</big></p>
<ul>
	<li>类名采用大驼峰命名法：ClassDemo</li>
	<li>函数方法名采用小驼峰命名法：myFunction</li>
	<li>变量名名采用下划线命名法：a_terrbile_project</li>
	<li>其余均按照PEP8格式</li>
</ul>

<p><big>图片文件路径</big></p>
<ul>
    <li>为了适配mac：image/xxx</li>
</ul>

<p><big>events/eyeTriacker/quest接口说明</big></p>
<ul>
    <li>clone(): 返回当前事件的深拷贝</li>
    <li>setAttributs(iterable): 设置变量，就是那个可以变蓝的东西</li>
    <li>getInfo(): 返回参数，字典类型</li>
    <li>setProperties(dict): 设置参数，也就是从文件导入的接口</li>
    <li>getDuration(): 返回事件的duration参数(ms)</li>
    <li>getUsingAttributes(): 返回使用中的attributes，列表类型</li>
    <li>getHiddenAttributes(): 返回隐藏属性，字典类型</li>
</ul>

<p><big>TODO</big></p>
<ul>
    <li>【done】单个事件获取timeline的attribute</li>
    <li>【done】事件绑定事件名</li>
    <li>【done】以timeline为单位的参数导入导出</li>
    <li>condition的条件判断</li>
</ul>

<p><big>关于导入导出的问题</big></p>
<ul>
    <li>timeline和cycle，调用save就可以得到数据</li>
    <li>调用restore，参数就是save得到的数据，就可以复原</li>
    <li>但是这个复原我阻止了发信号到structure，因为是structure的复原不会受到这个到影响</li>
    <li>对于if和switch的复制，之前返回的数据包含了一个类，已经被我修改为属性字典，测试正常</li>
</ul>
