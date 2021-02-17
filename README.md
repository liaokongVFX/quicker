# Quicker

![](readme/screenshot.gif)

## 简介
这个项目是一个类似于wox的快捷启动器。
项目使用python2.7构建，依赖了`PySide2`、`Apscheduler`、`requests`三个第三方库需要使用`pip`进行安装。

## 插件说明
1.translation action 是基于百度的api开发的，所以需要在secret_config中进行相关的api配置
2.everything plugin 是基于everything开发的，所以在使用时需要先打开everything软件，否则无法搜索到文件

## 插件编写
插件主要分为两类:`plugin`和`action`
### plugin插件
首先在`plugins`文件夹下建一个你插件名称的带有__init__.py文件的python包，
然后在包中的`__init__.py`文件写入入口类：
```python
from core import register
from core.plugin_base import AbstractPlugin
from result_item import ResultItem

@register  # 文件中可以写入多个类,但是使用register装饰器装饰过的类会被当做插件进行加载
class EverythingPlugin(AbstractPlugin):  # 插件需要继承AbstractPlugin父类
    title = u'搜索文件'     # 插件的名称（必填）
    description = u'需要打开everthing才能使用'  # 插件的描述（必填）
    keyword = 'find'    # 插件的关键字（必填）
    icon = ''   # 插件对应的图标路径，使用相对路径即可，比如这个包下面的img放了对应的图标icon.png,只需要写做 icon = 'img/icon.png'（选填）
    shortcut = ''  # 插件对应的快捷键 # 选填

    def run(self, text, result_item, plugin_by_keyword):
        """
        必须实现的方法，这个方法会在line edit回车或者下拉列表被点击时执行
        Args:
            text: line edit中的文字会按空格分成两个部分，text 就是空格后面的部分，比如cd python，那么text的值就是python
            result_item: 当前选中的下拉列表中的item
            plugin_by_keyword: 关键字和插件对象所组成的字典
        Returns: 这里只能返回两种情况，一种是什么也不返回，一种是返回ResultItem列表，返回ResultItem列表会被展示到下拉菜单中
        """
        pass

    def query(self, text):
        """
        非必须实现的方法，这个方法会在line edit文字修改时(textChanged)触发
        Args:
            text: ine edit中的文字会按空格分成两个部分，text 就是空格后面的部分，比如cd python，那么text的值就是python
        Returns: 这里只能返回两种情况，一种是什么也不返回，一种是返回ResultItem列表，返回ResultItem列表会被展示到下拉菜单中
        """
        pass

```


Plugin TODO
- [x] 添加网页搜索插件
- [x] 添加执行cmd命令插件
- [x] 添加截图插件
- [ ] 添加离线翻译插件
- [x] 集成everything
- [ ] 日事清插件（支持定时任务）
- [x] 添加打开路径插件

Action TODO
- [x] 划词翻译
- [x] 划词搜索
- [x] 划词设置提醒
- [x] 添加拾色插件