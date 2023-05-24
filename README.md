# MagicCube
这是一个用于识别和还原魔方的程序。

## Background
这个项目本身的目的是了解和学习程序开发的过程，同时学习相应的编程和工程知识。

本程序的目标是收集真实世界的魔方信息，并根据这些信息在程序中进行重现，然后还原并可视化这个过程。

## Principle
使用传统算法识别魔方的一个面，对图片进行预处理，先找到魔方一个面9个贴纸的轮廓，再通过轮廓位置匹配对应贴纸颜色。在六个面都识别成功后，根据魔方特性将所得的魔方展开图进行处理，使之与现实魔方匹配。完成后将魔方可视化并进行还原，其中还原算法采用Python自带的库，可视化部分采用传统建模。

## Platform
Windows

## Install
将此仓库克隆到本地。

```
$ git clone https://github.com/2820207922/MagicCube.git
```

运行以下代码来安装依赖项。 在此之前推荐使用Conda创建虚拟环境。

```
$ pip install -r requirements
```

## Usage
找到文件 ```visualization.py``` 并运行。稍等片刻，您将看到以下屏幕。

![image](example/e1.png)

单击最右侧的按钮。 你会看见

![image](example/e2.png)

将魔方对准相机，按下空格键完成抓拍。

![image](example/e3.png)

如果捕捉时发现颜色不准确，按c进入校正模式，然后依次校正。

![image](example/e4.png)

然后依次捕获6个面，请确保每个面都是正确。

![image](example/e5.png)

按回车键自动完成各面的归位。

![image](example/e6.png)

按esc退出，完成以上步骤后你会发现你的魔方已经被复制了。 单击播放按钮将开始还原。

![image](example/e7.png)
![image](example/e8.png)
![image](example/e9.png)

最后，你的魔方就解开了。 您可以在下图中查看更多功能。

![image](example/e10.png)
![image](example/e11.png)
