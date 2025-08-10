# 2025/5/17
使用列表存储角色的每一个动作，在循环中跳到下一个动作。

```python

actions = [run, jump, shoot, hide]

for act in actions:
    act()

```