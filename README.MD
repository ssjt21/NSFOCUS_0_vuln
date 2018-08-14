# 用于批量生成指定主机没有漏洞的报告 --NSFOCUS
  -  图爿的路径为 images/主机数量.png
  - 图片需要自己生成，这里没有办法生成和是扫描报告中一样的图片

# 使用python2 环境

 - jinja2

# 使用方法
  - 请手动指定IP文件夹路径 ：
 ```python
#需要批量处理的资产路径
ASSET_DIR='assets'
```
 - 文件每个文当(xxx.txt)
 - 文档中的格式
 ```
 ip1   windows
 ip2   linux
 ```

