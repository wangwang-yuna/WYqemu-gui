# QEMU GUI

这是一个基于 Python 的图形用户界面 (GUI) 应用程序，用于简化 QEMU 虚拟机的配置和管理。用户可以方便地指定 QEMU 路径、虚拟机镜像文件以及各种配置选项，如 CPU 核心数、内存大小和网络设置。

## 特性

- 检测 QEMU 版本，并提供安装脚本。
- 提供图形界面用于输入 QEMU 路径、虚拟机镜像和配置选项。
- 允许用户选择网络配置，包括用户网络、桥接网络和主机网络。
- 支持保存和加载配置文件（使用 YAML 格式）。
- 提供命令行执行功能，可以在 GUI 内执行任意命令。
- 日志记录功能，记录操作和错误信息。

## 环境要求

- Python 3.x
- 自动安装所需库
- QEMU（请确保在系统中安装并可用）

## 使用方法

1. 克隆或下载此项目到本地计算机。
2. 进入项目目录。
3. 安装所需的 Python 库（如果尚未安装）

## 日志与错误处理
日志文件将被保存在 log 目录中，文件名为 UUID 格式。运行期间的所有输出和错误信息会被记录到日志中，方便后续的查阅。

## 注意事项
- 请确保 QEMU 的可执行文件在指定的路径下。
- 对于桥接网络，请确保提供有效的网络接口名称。
- 对于主机网络，请确保提供有效的 IP 地址和网关。
- 只支持linux系统，windows系统请自个开发去，反正理论上是可以运行的

## 贡献
就只有开发者一个人喵喵喵
