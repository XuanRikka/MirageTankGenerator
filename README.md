# 幻影坦克生成器
为了解决自己一些需求写的一个简单的幻影坦克图片生成器

## 用法
```
MirageTankGenerator <inner_path: str> <outer_path: str> 
把两张图片合成为一张幻影坦克
用法:
inner_path为里图路径，outer_path为表图路径

可用的选项有:
* 表图亮度调节系数，必须在0-1之间，默认为1.0
  --inner-light <inner_light: float> 
* 里图亮度调节系数，必须在0-1之间，默认为0.3
  --outer-light <outer_light: float> 
* 输出文件路径，只能为webp/png/bmp
  -o│--output <output_path: str> 
* OpenCV使用CPU多线程的核心数，设置为0则禁用多线程
  -c│--cpu-num <cpu_num: str> 
* 是否禁用OpenCV使用OpenCL
  -d-ocl│--disable-opencl 
* 放大时使用的算法，缩小时无效，默认为cubic
  --interp <interp: 'lanczos4'|'cubic'|'linear'|'nearest'> 
* 输出的图片使用表图的分辨率，默认使用里图的分辨率
  --use-outer 

使用示例:
MirageTankGenerator.exe aaa.png bbb.png --output ccc.png
```

## 示例

### 里图
![里图](example/test1.jpg)
### 表图
![表图](example/test2.jpg)
### 幻影坦克
![幻影坦克](example/output.png)


## 鸣谢

- [leinlin老师的幻影坦克架构指南系列](https://zhuanlan.zhihu.com/p/31164700)
- [MirageTankGo](https://github.com/Aloxaf/MirageTankGo)

