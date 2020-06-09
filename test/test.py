import sys
from collections import namedtuple
# 核心类
# 用于读取YAML和JSON格式的文件
from ansible.parsing.dataloader import DataLoader
# 用于存储各类变量信息
from ansible.vars.manager import VariableManager
# 用于导入资产文件
from ansible.inventory.manager import InventoryManager


# InventoryManager类的调用方式
def InventoryManagerStudy():
    dl = DataLoader()
    # loader= 表示是用什么方式来读取文件  sources=就是资产文件列表，里面可以是相对路径也可以是绝对路径
    im = InventoryManager(loader=dl, sources=["hosts"])

    # 获取指定资产文件中所有的组以及组里面的主机信息，返回的是字典，组名是键，主机列表是值
    allGroups = im.get_groups_dict()
    print(allGroups)

    # 获取指定组的主机列表
    print(im.get_groups_dict().get("test"))

    # 获取指定主机，这里返回的是host的实例
    host = im.get_host("172.16.48.242")
    print(host)
    # 获取该主机所有变量
    print(host.get_vars())
    # 获取该主机所属的组
    print(host.get_groups())


def main():
    InventoryManagerStudy()


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit()