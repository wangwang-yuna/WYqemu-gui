echo "开始安装qemu-system"
echo "sudo将持续安装过程........"
sudo apt-get install qemu-system qemu-user-static
echo "开始安装python3"
sudo apt-get install python3 python3-pip python3-venv python3-tk
echo "创建虚拟环境"
python3 -m venv ~/.base
echo "激活虚拟环境"
source ~/.base/bin/activate
echo "安装pip依赖包"
echo "是否使用清华源？"
read answer
if [ "$answer" == "y" ]; then
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
pip install -r requirements.txt
echo "安装完成"
else
pip install -r requirements.txt
echo "安装完成"