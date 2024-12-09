echo "是否删除WYqemu-gui？"
read answer
if [ "$answer" == "y" ]; then
    cd ..
    rm -rf WYqemu-gui
    echo "WYqemu-gui已删除"
    echo "是否删除WYqemu-gui依赖的qemu？"
    read answer
    if [ "$answer" == "y" ]; then
        sudo apt autoremove qemu-system
        echo "qemu-system已删除"
    fi
fi