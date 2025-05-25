import pygame
import weakref
from enum import Enum
import math,time
from pygame.locals import *
from collections import defaultdict

# 初始化Pygame
pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
CLOCK = pygame.time.Clock()
FPS = 60

class T:
    def __init__(self, value):
        self.value = value

    # 隐式转换核心逻辑
    def _to_number(self, x):
        if isinstance(x, T):
            x = x.value
        if isinstance(x, bool):
            return 1.0 if x else 0.0
        try:
            return float(x)
        except (ValueError, TypeError):
            return 0.0  # 所有无效转换返回 0

    def _to_string(self, x):
        if isinstance(x, T):
            x = x.value
        return str(x)

    # 重载操作符
    def __add__(self, other):
        # Scratch 的 +：优先字符串拼接
        if isinstance(self.value, str) or isinstance(other, str):
            return T(self._to_string(self.value) + self._to_string(other))
        return T(self._to_number(self.value) + self._to_number(other))

    def __sub__(self, other):
        # Scratch 的 -：强制转数字
        return T(self._to_number(self.value) - self._to_number(other))

    def __mul__(self, other):
        # Scratch 的 *：强制转数字
        return T(self._to_number(self.value) * self._to_number(other))

    def __truediv__(self, other):
        # Scratch 的 /：强制转数字，除零返回 inf
        return T(self._to_number(self.value) / self._to_number(other))

    # 比较操作符
    def __eq__(self, other):
        # Scratch 的 ==：松散比较
        if isinstance(other, T):
            other = other.value
        return self.value == other

    # 类型转换方法
    def as_number(self):
        return self._to_number(self.value)

    def as_string(self):
        return self._to_string(self.value)

    def __repr__(self):
        return f"T({repr(self.value)})"

    # 支持布尔上下文（if 语句）
    def __bool__(self):
        return bool(self.value)
    
# 全局资源管理器
class ResourceManager:
    _cache = weakref.WeakValueDictionary()
    
    @classmethod
    def load_image(cls, path):
        if path not in cls._cache:
            cls._cache[path] = pygame.image.load(path).convert_alpha()
        return cls._cache[path]

# 事件类型定义
class GameEvent(Enum):
    BROADCAST = pygame.USEREVENT + 1
    COLLISION = pygame.USEREVENT + 2
    CLONE = pygame.USEREVENT + 3

class TaskType(Enum):
    WAIT = 1
    BROADCAST = 2
    CHANGE_VAR = 3
    SWITCH_COSTUME = 4
    LOOP = 5

# 核心Sprite类
class ScratchSprite(pygame.sprite.Sprite):
    __slots__ = [
        'image', 'rect', 'costumes', 'current_costume', 
        '_direction', '_x', '_y', 'size', 'visible',
        '_move_components', '_broadcast_listeners', '_pen_props'
    ]
    
    def __init__(self, costumes, start_pos=(0, 0)):
        super().__init__()
        
        # 图像属性
        self.costumes = [ResourceManager.load_image(c) for c in costumes]
        self.current_costume = 0
        self.image = self.costumes[self.current_costume]
        self.rect = self.image.get_rect(center=start_pos)
        self.visible = True
        self.size = 100  # 百分比
        
        # 运动属性
        self._direction = 90  # Scratch标准方向（0=向上）
        self._x, self._y = start_pos
        self.speed = 0
        
        # 事件系统
        self._broadcast_listeners = defaultdict(list)
        
        # 物理属性
        self.bounce_on_edge = False
        self.rotation_style = 'all around'  # 'left-right'/'none'
        
        # 组件系统
        self._move_components = {
            'glide': None,
            'move_steps': None
        }
        
        # 画笔系统
        self._pen_props = {
            'pen_down': False,
            'color': (0,0,0),
            'size': 1
        }
        # 新增任务系统
        self.task_queue = []          # 待执行任务队列
        self.current_task = None      # 当前执行任务
        self.task_start_time = 0      # 任务开始时间
        self.loop_counter = {}        # 循环计数器
        
        # 内置变量存储
        self.variables = {
            'global': {},
            'local': {}
        }

    # 新增任务管理方法 -----------------------------------------
    def add_task(self, task_type, **kwargs):
        """ 添加任务到队列 """
        task = {
            'type': task_type,
            'params': kwargs,
            'completed': False
        }
        self.task_queue.append(task)

    def _process_tasks(self):
        """ 处理任务队列 """
        if not self.current_task and self.task_queue:
            self.current_task = self.task_queue.pop(0)
            self.task_start_time = time.time()

        if self.current_task:
            task = self.current_task
            handler = getattr(self, f'_handle_{task["type"].name.lower()}', None)
            if handler and not task['completed']:
                task['completed'] = handler(**task['params'])

            if task['completed']:
                self.current_task = None

    # 任务处理器 ----------------------------------------------
    def _handle_wait(self, seconds):
        """ 等待指定秒数 """
        elapsed = time.time() - self.task_start_time
        return elapsed >= seconds

    def _handle_broadcast(self, message):
        """ 发送广播 """
        self.broadcast(message)
        return True  # 立即完成

    def _handle_change_var(self, name, value, scope='local'):
        """ 修改变量 """
        self.variables[scope][name] = value
        return True

    def _handle_switch_costume(self, index):
        """ 切换造型 """
        self.switch_costume(index)
        return True

    def _handle_loop(self, count, tasks):
        """ 循环执行任务 """
        loop_id = id(tasks)
        self.loop_counter.setdefault(loop_id, 0)
        
        if self.loop_counter[loop_id] < count:
            if not self.task_queue or self.task_queue[0] != tasks[0]:
                self.task_queue = tasks.copy() + self.task_queue
            self.loop_counter[loop_id] += 1
            return False
        else:
            del self.loop_counter[loop_id]
            return True

    # 更新方法扩展 --------------------------------------------
    def update(self, dt, events):
        super().update(dt, events)
        self._process_tasks()  # 处理自主任务

    # 核心方法 --------------------------------------------------
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.centerx = int(value)
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.rect.centery = int(value)
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value):
        self._direction = value % 360
        if self.rotation_style == 'left-right':
            self.image = pygame.transform.flip(
                self.costumes[self.current_costume], 
                self._direction > 90 and self._direction < 270, 
                False
            )
        elif self.rotation_style == 'all around':
            self.image = pygame.transform.rotate(
                self.costumes[self.current_costume], 
                -self._direction + 90
            )
        self.rect = self.image.get_rect(center=self.rect.center)

    # 运动控制 --------------------------------------------------
    def move(self, steps):
        rad = math.radians(-self.direction + 90)
        self.x += steps * math.cos(rad)
        self.y += steps * math.sin(rad)
        self._check_edge()

    def glide_to(self, target, duration):  # 单位：毫秒
        self._move_components['glide'] = {
            'start_pos': (self.x, self.y),
            'target_pos': target,
            'duration': duration,
            'start_time': pygame.time.get_ticks()
        }

    def point_towards(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        self.direction = math.degrees(math.atan2(-dy, dx)) + 90

    # 外观控制 --------------------------------------------------
    def switch_costume(self, name_or_index):
        if isinstance(name_or_index, int):
            self.current_costume = name_or_index % len(self.costumes)
        else:
            # 假设costumes是带名字的列表（此处需要扩展）
            pass
        self.image = self.costumes[self.current_costume]
        self.rect = self.image.get_rect(center=self.rect.center)

    def change_size(self, percent):
        orig_rect = self.image.get_rect()
        new_size = (orig_rect.width * percent//100, 
                   orig_rect.height * percent//100)
        self.image = pygame.transform.scale(self.costumes[self.current_costume], new_size)
        self.rect = self.image.get_rect(center=self.rect.center)

    # 事件系统 --------------------------------------------------
    def broadcast(self, message):
        event = pygame.event.Event(GameEvent.BROADCAST.value, {'message': message})
        pygame.event.post(event)

    def on_broadcast(self, message, callback):
        self._broadcast_listeners[message].append(callback)

    def _handle_events(self, events):
        for event in events:
            if event.type == GameEvent.BROADCAST.value:
                if event.message in self._broadcast_listeners:
                    for cb in self._broadcast_listeners[event.message]:
                        cb()

    # 克隆系统 --------------------------------------------------
    def create_clone(self):
        clone = self.__class__(self.costumes, (self.x, self.y))
        event = pygame.event.Event(GameEvent.CLONE.value, {'clone': clone})
        pygame.event.post(event)
        return clone

    # 物理检测 --------------------------------------------------
    def _check_edge(self):
        if self.bounce_on_edge:
            if not (0 <= self.x <= SCREEN.get_width()):
                self.direction = 180 - self.direction
            if not (0 <= self.y <= SCREEN.get_height()):
                self.direction = -self.direction

    def touching(self, other):
        return self.rect.colliderect(other.rect)

    # 更新逻辑 --------------------------------------------------
    '''def update(self, dt, events):
        self._handle_events(events)
        
        # 处理移动组件
        if self._move_components['glide']:
            glide = self._move_components['glide']
            progress = (pygame.time.get_ticks() - glide['start_time']) / glide['duration']
            
            if progress >= 1:
                self.x, self.y = glide['target_pos']
                self._move_components['glide'] = None
            else:
                self.x = glide['start_pos'][0] + (glide['target_pos'][0] - glide['start_pos'][0]) * progress
                self.y = glide['start_pos'][1] + (glide['target_pos'][1] - glide['start_pos'][1]) * progress
        
        if self.speed != 0:
            self.move(self.speed * dt / 1000)
        
        # 画笔处理
        if self._pen_props['pen_down']:
            pygame.draw.circle(SCREEN, self._pen_props['color'], 
                             (int(self.x), int(self.y)), self._pen_props['size'])'''
