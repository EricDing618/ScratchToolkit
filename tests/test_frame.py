import os
os.chdir(os.path.dirname(__file__))
#from scratchtoolkit.__STP.frame.spriteframe import *

class TestSpriteFrame:
    def test_sprite_frame(self):
        '''# 创建角色
        sprite1 = ScratchSprite(['cat.png', 'cat_walk.png'], (400, 300))
        sprite1.speed = 2
        sprite1.bounce_on_edge = True
        
        # 设置广播监听
        def switch_costume():
            sprite1.current_costume = (sprite1.current_costume + 1) % 2
            sprite1.switch_costume(sprite1.current_costume)
        
        sprite1.on_broadcast('switch', switch_costume)
        dt = CLOCK.tick(FPS)
        events = pygame.event.get()
        
        # 初始化角色
        A = ScratchSprite(['a1.png', 'a2.png'], (100, 100))
        B = ScratchSprite(['b.png'], (200, 200))
        C = ScratchSprite(['c.png'], (300, 300))
        D = ScratchSprite(['d1.png', 'd2.png', 'd3.png'], (400, 400))

        # 配置角色自主任务
        # A - 等待1秒后切换造型
        A.add_task(TaskType.WAIT, seconds=1)
        A.add_task(TaskType.SWITCH_COSTUME, index=1)

        # B - 立即发送广播
        B.add_task(TaskType.BROADCAST, message="ALERT")

        # C - 修改全局变量
        C.add_task(TaskType.CHANGE_VAR, name="score", value=100, scope="global")

        # D - 循环3次切换造型（使用复合任务）
        loop_tasks = [
            {'type': TaskType.SWITCH_COSTUME, 'params': {'index': 1}},
            {'type': TaskType.WAIT, 'params': {'seconds': 0.5}},
            {'type': TaskType.SWITCH_COSTUME, 'params': {'index': 2}},
            {'type': TaskType.WAIT, 'params': {'seconds': 0.5}}
        ]
        D.add_task(TaskType.LOOP, count=3, tasks=loop_tasks)

        # 主循环
        running = True
        while running:
            # ...事件处理...
            dt = CLOCK.tick(FPS)
            events = pygame.event.get()
            
            for event in events:
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        sprite1.broadcast('switch')
                    elif event.key == K_c:
                        clone = sprite1.create_clone()
            
            # 更新所有精灵
            all_sprites = pygame.sprite.Group(sprite1)  # 实际使用时需要管理克隆体
            
            all_sprites.update(dt, events)
            
            # 渲染
            SCREEN.fill((255,255,255))
            all_sprites.draw(SCREEN)
            pygame.display.flip()

        pygame.quit()
        
'''
        while True: a=1+1
        #assert 1==2