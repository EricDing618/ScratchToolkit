<div align="center">

![logo](./res/logo.svg)  

# ScratchToolkit
![GitHub Repo stars](https://img.shields.io/github/stars/EricDing618/Scratch-To-Pygame?style=flat)
![GitHub branch status](https://img.shields.io/github/checks-status/EricDing618/Scratch-To-Pygame/main)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/EricDing618/Scratch-To-Pygame)
![GitHub last commit](https://img.shields.io/github/last-commit/EricDing618/Scratch-To-Pygame)
![GitHub Created At](https://img.shields.io/github/created-at/EricDing618/Scratch-To-Pygame)  

</div>

## STP: Scratch-To-Pygame
### 描述
- Scratch-To-Pygame（STP）是一个用Python实现的将Scratch转换为Pygame的脚本工具，现已支持`.sb3`文件。
### 快速使用
在本仓库目录下使用`cmd`执行：
```bash
python ./src/stp.py -c <目标.sb3文件路径>
```
更多使用方法：
- `-h`和`--help`：显示命令帮助列表。
- `-r`和`--run`：转换完毕后自动执行output文件。
- `-nl`和`--no-log`：不显示输出日志。  
- `-c`和`--convert`：指定转换目标`.sb3`文件路径。
- `-sl`和`--save-log`：保存输出日志到文件。
- `-rmlog`和`--remove-log`：删除输出日志文件的个数。（按照时间顺序，值为0表示所有日志）
- `-t`和`--tree`：输出转换脚本的代码树信息。（一般用于出现问题时排查，使开发者更容易定位问题，建议在提交bug时附带此信息）
- `-st`和`--save-tree`：保存转换脚本的代码树信息到文件。

例：
```bash
python ./src/stp.py -c ./../../tests/allblocks.sb3 --run -sl --tree -st
```

> [!WARNING]
> - 将不考虑支持以下功能：
>   - 变量、列表显示功能
>   - 云变量功能
>   - “说”“思考”“询问...并等待”显示功能（或考虑使用`print()`及`input()`函数）
>   - 除画笔、音乐以外的Scratch3扩展功能  
>  - 作者将只在turbowarp上进行测试，任何在scratch3上出现但在turbowarp上没有的问题请等待他人解答

> [!TIP]
> 你可以提交Issue，但[EricDing618](https://github.com/EricDing618)可能会忽略它，需要等待他人的PR。

## pack.py
### 描述
- pack.py是一个将解包后的Scratch项目还原的脚本。
## merge.py
### 描述
- merge.py是一个将两个`.sb3`文件合并为一个文件的脚本。
# 安装依赖
- 在根目录下执行：  
```bash
pip install -r requirements.txt
```
- 解压并安装`dependencies`分支下的软件（仅支持Windows x64）。
## 报错解决
- `ImportError`：详见**第三方库&软件**。

若这仍不能解决您的问题，请确保该问题没有在issues被提出并解决，然后创建issue并等待解决。