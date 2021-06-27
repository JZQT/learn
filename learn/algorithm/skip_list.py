# coding: utf-8
"""跳跃表的实现"""
from __future__ import annotations

from typing import List, Optional, Any
from random import randint

_MAX_LEVEL = 32  # 跳跃表最大索引指针层数
_MAX_RANDOM_NUMBER = 2 ** (_MAX_LEVEL - 1) - 1  # 最大随机数，用于概率性分配索引指针层数


def random_level() -> int:
    """随机分配跳跃表节点的索引指针层数"""
    level = 1  # 至少包含 1 层索引指针
    # 随机数 number 从低位开始每一位表示是否分配下一层索引指针
    number = randint(0, _MAX_RANDOM_NUMBER)
    while level < _MAX_LEVEL and (number & 1) == 1:
        level += 1
        number = number >> 1
    return level


class SkipListNode(object):
    next: List[Optional[SkipListNode]]  # 指向后面节点的索引指针列表
    data: Any  # 节点存储的数据

    def __init__(self, data):
        """跳跃表节点初始化"""
        self.data = data
        self.next = [None for _ in range(random_level())]


class SkipList(object):
    """单向跳跃表实现"""
    next: List[Optional[SkipListNode]]  # 指向后面节点的索引指针列表

    def __init__(self):
        """跳跃表初始化"""
        self.next = [None for _ in range(_MAX_LEVEL)]

    def search(self, data):
        """根据数据值查找并返回数据

        数据值没有的话返回 None，跳表包含相同数据值会返回最后一个数据。
        """
        # 从最高层索引指针开始，往下找到第一个不大于待查找数据的节点
        level = len(self.next) - 1  # 当前要查找的索引层级
        while level > -1 and (self.next[level] is None or self.next[level].data > data):
            level -= 1

        # 针对空跳跃表情况下的处理，这种情况下所有索引指针都指向空
        if level < 0:
            return None

        curr_node = self.next[level]
        while level > -1:
            next_node = curr_node.next[level]
            if next_node is None or next_node.data > data:
                level -= 1
                continue
            curr_node = next_node

        return curr_node.data if curr_node.data == data else None

    def insert(self, data):
        """插入数据

        如果跳表包含相同数据值的话，会插入到相同数据值的最后面
        """
        node = SkipListNode(data)  # 待插入节点
        level = len(self.next) - 1  # 当前要查找的索引层级
        while level > -1 and (self.next[level] is None or self.next[level].data > data):
            # 当前 self 到 self.next[level] 属于要插入的数据节点范围
            # 如果新节点包含该层索引，那么建立新的链接
            if level < len(node.next):
                node.next[level] = self.next[level]
                self.next[level] = node
            level -= 1

        # 这种情况下数据已作为第一个节点插入完毕
        if level < 0:
            return

        curr_node = self.next[level]
        while level > -1:
            next_node = curr_node.next[level]
            if next_node is None or next_node.data > data:
                # 当前 curr_node 到 next_node 属于要插入的数据节点范围
                # 如果新节点包含该层索引，那么建立新的链接
                if level < len(node.next):
                    node.next[level] = next_node
                    curr_node.next[level] = node
                level -= 1
                continue
            curr_node = next_node

    def delete(self, data):
        """删除数据

        如果跳表包含相同数据值的话，会删除第一个相同数据值
        """
        next_list = []  # 以栈的方式记录可能要做断开操作的索引指针列表供回溯

        # 从最高层索引指针开始，往下找到第一个不大于等于待查找数据的节点
        level = len(self.next) - 1  # 当前要查找的索引层级
        while level > -1 and (self.next[level] is None or self.next[level].data >= data):
            next_list.append(self.next)  # 记录存储当前层链接的索引指针列表，供回溯
            level -= 1

        if level < 0:
            first_node = self.next[0]
            # 待删除节点是第一个数据节点
            if first_node is not None and first_node.data == data:
                self._delete_node(first_node, next_list)
            return

        curr_node = self.next[level]
        while level > -1:
            next_node = curr_node.next[level]
            if next_node is None or next_node.data >= data:
                next_list.append(curr_node.next)  # 记录存储当前层链接的索引指针列表，供回溯
                level -= 1
                continue
            curr_node = next_node

        # 找到待删除的节点
        if curr_node.next[0] is not None and curr_node.next[0].data == data:
            self._delete_node(curr_node.next[0], next_list)

    @staticmethod
    def _delete_node(node: SkipListNode, next_list: List[List[Optional[SkipListNode]]]):
        """删除查找到的跳跃表节点"""
        level = 0  # 从底层开始进行索引链接断开处理
        # 删除节点，并回溯断开对应层索引指针链接
        while level < len(node.next):
            curr_next = next_list.pop()  # 从底层开始依次找到需要断开的链接进行处理
            curr_next[level] = node.next[level]  # 断开并重建索引指针
            level += 1
