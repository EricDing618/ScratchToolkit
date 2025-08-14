from typing import List, Dict, Any, Set, Iterator, Union
from dataclasses import dataclass
from src.utils.objects import Block

@dataclass
class Change: pass

@dataclass
class Add(Change):
    block: 'Block'

@dataclass
class Reduce(Change):
    block: 'Block'

@dataclass
class Modify(Change):
    old_block: 'Block'
    new_block: 'Block'
    changed_attrs: Dict[str, Any]

@dataclass
class Unchanged(Change):
    block: 'Block'

class Block:
    def __init__(self, id: str, **kwargs):
        self.id = id
        self.opcode = kwargs.get('opcode', '')
        self.next = kwargs.get('next', None)
        self.parent = kwargs.get('parent', None)
        self.inputs = kwargs.get('inputs', {})
        self.fields = kwargs.get('fields', {})
        self.shadow = kwargs.get('shadow', False)
        self.topLevel = kwargs.get('topLevel', False)
        self.x = kwargs.get('x', None)
        self.y = kwargs.get('y', None)
        self.isHead = all([self.x, self.y])

    def __repr__(self):
        return f"Block(id={self.id!r}, opcode={self.opcode!r}, ...)"

# 硬编码需要比较的属性（排除 x, y）
COMPARE_ATTRS = {'opcode', 'next', 'parent', 'inputs', 'fields', 'shadow', 'topLevel', 'isHead'}

def compare_blocks_optimized(
    old_blocks: List[Block],
    new_blocks: List[Block],
    ignore_attrs: Set[str] = {'x', 'y'}
) -> Iterator[Change]:
    """
    高效比较两个 Block 列表，返回变更迭代器（内存优化）。
    
    Args:
        old_blocks: 旧 Block 列表
        new_blocks: 新 Block 列表
        ignore_attrs: 要忽略的属性
    
    Yields:
        Change: Add/Reduce/Modify/Unchanged 实例
    """
    old_dict = {b.id: b for b in old_blocks}
    new_dict = {b.id: b for b in new_blocks}

    # 先处理新增的 Block
    for block_id, new_block in new_dict.items():
        if block_id not in old_dict:
            yield Add(new_block)

    # 再处理删除和修改的 Block
    for block_id, old_block in old_dict.items():
        if block_id not in new_dict:
            yield Reduce(old_block)
        else:
            new_block = new_dict[block_id]
            changed_attrs = {}
            
            # 仅比较指定的属性（提前终止）
            for attr in COMPARE_ATTRS - ignore_attrs:
                old_val = getattr(old_block, attr, None)
                new_val = getattr(new_block, attr, None)
                if old_val != new_val:
                    changed_attrs[attr] = (old_val, new_val)
                    break  # 只要有一个不同就标记为修改
            
            if changed_attrs:
                yield Modify(old_block, new_block, changed_attrs)
            else:
                yield Unchanged(old_block)