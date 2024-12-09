echo "是否一件删除日志文件？(y/n)"
read answer
if [ "$answer" == "y" ]; then
    rm -rf ./log/
    echo "日志文件已删除！" 
else
    echo "取消删除！"
    fi
    echo "是否删除config文件？(y/n)"
    read answer
    if [ "$answer" == "y" ]; then
        rm -rf ./configs/
        echo "config文件已删除！" 
    else
        echo "取消删除！"
    fi