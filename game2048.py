# -*- coding: utf-8 -*-
__author__ = 'zl'

import random
import os
import sys
#from pynput.keyboard import Key


class ArrayValue:
    """
    二维数组
    """
    def __init__(self, side):
        self.side = side
        self.cur_id = None
        self.cur_x = None
        self.cur_y = None
        self.max_val = None
        self.blank_arr = []
        self.array = None
        self._init_array()
        self.lst_map = {'left': range(self.side),
                        'right': range(self.side)[::-1],
                        'up': range(self.side),
                        'down': range(self.side)[::-1]}

    # 初始化二维数组
    def _init_array(self, max_value=2):
        # 生成不大于max_value的所有平方数
        # power = [0, 2, 4]
        self.array = [[0 for _ in range(self.side)] for _ in range(self.side)]
        self.cur_id = random.randint(0, 15)
        # 根据ID 赋值cur_x, cur_y
        self._set_x_y()
        self.max_val = 2
        # set value
        self.array[self.cur_x][self.cur_y] = 2

    # 根据ID 设置cur_x cur_y
    def _set_x_y(self):
        self.cur_x = self.cur_id % 4
        self.cur_y = self.cur_id / 4

    def _get_x_y(self):
        return self.cur_x, self.cur_y

    # 根据cur_x cur_y获取ID
    def _get_id(self):
        return self.cur_y * 4 + self.cur_x

    # 根据ID获取value
    def get_val(self, tmp_id):
        tmp_x = tmp_id % 4
        tmp_y = tmp_id / 4
        return self.array[tmp_x][tmp_y]

    # 设置某ID的value
    def set_val(self, tmp_id, val):
        tmp_x = tmp_id % 4
        tmp_y = tmp_id / 4
        self.array[tmp_x][tmp_y] = val

    def get_array(self):
        return self.array

    # 刷新空白array
    def refresh_blank(self):
        bland_arr = []
        for i in range(self.side):
            for j in range(self.side):
                if self.array[i][j] == 0:
                    bland_arr.append(i+4*j)
        self.blank_arr = bland_arr

    # 刷新最大值
    def refresh_max(self, num):
        if num > self.max_val:
            self.max_val = num

    # 空位新生
    def new_rand(self):
        choice = random.choice(self.blank_arr)
        # 新生值不超过当前最大值
        new_value = random.choice(get_all_power(self.max_val))
        # 算了，不超过最大值的一半吧
        if new_value > 2:
            new_value = new_value/2
        self.set_val(choice, new_value)
        self.cur_x = choice % 4
        self.cur_y = choice/4


class Grid(ArrayValue):
    def __init__(self, my_side, my_id):
        # super
        ArrayValue.__init__(self, my_side)

        self.id = my_id
        # init coord
        self._init_coord(self.id)
        # draw coord
        init_array = self.get_array()
        self.draw_coord(array=init_array)

    def _init_coord(self, my_id):
        # check id legal
        if my_id not in range(16):
            raise Exception('Grid id out of range 0,15')
        x = my_id % 4
        if x == 0:
            x = 4
        self.x = x
        self.y = my_id/4 + 1

    def draw_coord(self, array):
        # The first raw line
        print ' ____ ' * self.side
        for i in range(self.side):
            # flag if delete one space, the last time if curx cury true
            flag = False
            # The first column
            print '|',
            # straight right vertical
            for j in range(self.side):
                _space = '    '
                if flag:
                    _space = '   '
                    flag = False

                # highlight
                if i == self.cur_x and j == self.cur_y:
                    flag = True
                    print '\033[0;31;40m',
                    _space = '  '

                value = ''
                int_value = array[i][j]
                if int_value != 0:
                    value = int_value
                value = str(value)
                value = _space + value
                value = value[-4:]
                print '%s|' % value,

                # cancel highlight
                if i == self.cur_x and j == self.cur_y:
                    print '\033[0m',

            # straight right crossing
            print
            print '| ____' * self.side

    def move(self, direction):
        if direction in ['left', 'right']:
            self. _horizontal_move(direction)
        elif direction in ['down', 'up']:
            self._vertical_move(direction)
        else:
            raise Exception('no ... fuck you!!!')

    # 水平移动
    def _horizontal_move(self, dire):
        for ix in range(self.side):
            self._horizontal_move_single(dire, ix)
            self._horizontal_add_single(dire, ix)

    # 单组水平移动
    def _horizontal_move_single(self, dire, x):
        # 先把所有数字向边上移动,al
        # copy一个数组
        copy_arr = self.array[:]
        # 新初始化的数组，全为0
        new_arr = [0 for _ in range(self.side)]
        for iy in self.lst_map[dire]:
            if copy_arr[x][iy]:
                if dire == 'left':
                    replace_zero(new_arr, copy_arr[x][iy])
                elif dire == 'right':
                    replace_zero(new_arr, copy_arr[x][iy], asc=False)
        self._replace_arr_x(self.array, x, new_arr)

    # 单组水平相加
    def _horizontal_add_single(self, dire, x):
        tmp = 0
        for i in self.lst_map[dire]:
            if tmp and tmp == self.array[x][i]:
                if dire == 'left':
                    # 赋值
                    self.array[x][i - 1] = tmp * 2
                    # 比较最大值
                    self.refresh_max(tmp*2)
                elif dire == 'right':
                    # 赋值
                    self.array[x][i + 1] = tmp * 2
                    # 比较最大值
                    self.refresh_max(tmp * 2)
                # 置0
                self.array[x][i] = 0
                # 水平移动
                self._horizontal_move_single(dire, x)
            tmp = self.array[x][i]

    # 竖直移动
    def _vertical_move(self, dire):
        for iy in range(self.side):
            self._vertical_move_single(dire, iy)
            self._vertical_add_single(dire, iy)

    def _replace_arr_x(self, arr2, x, new_arr):
        for i in range(self.side):
            arr2[x][i] = 0
        for i in range(len(new_arr)):
            arr2[x][i] = new_arr[i]

    def _replace_arr_y(self, arr2, y, new_arr):
        for i in range(self.side):
            arr2[i][y] = 0
        for i in range(len(new_arr)):
            arr2[i][y] = new_arr[i]

    # 单组竖直移动
    def _vertical_move_single(self, dire, y):
        # 先把所有数字向边上移动,al
        # copy一个数组
        copy_arr = self.array[:]
        # 新初始化的数组，全为0
        new_arr = [0 for _ in range(self.side)]
        for ix in self.lst_map[dire]:
            if copy_arr[ix][y]:
                if dire == 'up':
                    replace_zero(new_arr, copy_arr[ix][y])
                elif dire == 'down':
                    replace_zero(new_arr, copy_arr[ix][y], asc=False)
        self._replace_arr_y(self.array, y, new_arr)

    # 相加
    def _vertical_add_single(self, dire, y):
        tmp = 0
        for i in self.lst_map[dire]:
            if tmp and tmp == self.array[i][y]:
                if dire == 'up':
                    # 赋值
                    self.array[i-1][y] = tmp * 2
                    # 比较最大值
                    self.refresh_max(tmp * 2)
                elif dire == 'down':
                    # 赋值
                    self.array[i+1][y] = tmp * 2
                    # 比较最大值
                    self.refresh_max(tmp * 2)
                # 置0
                self.array[i][y] = 0
                # 移动
                self._vertical_move_single(dire, y)
            tmp = self.array[i][y]

    def refresh(self):
        if 'windows' in sys.platform.strip():
            os.system('cls')
        elif 'linux' in sys.platform.strip():
            os.system('clear')
        self.draw_coord(self.array)


# 获取所有小于m的2的幂
def get_all_power(m):
    power_list = [2]
    i = 2
    while True:
        i = i * 2
        if i > m:
            break
        power_list.append(i)
    return power_list


# 替换arr边上的0为num
def replace_zero(arr, num, asc=True):
    idx_lst = range(len(arr))
    if not asc:
        idx_lst = idx_lst[::-1]
    for i in idx_lst:
        if not arr[i]:
            arr[i] = num
            break


def main():
    """
    1、初始化
    2、移动相加
    3、获取空位
    4、空位新生
    5、重复2-4
    """
    g = Grid(4, 1)
    dir_map = {'a': 'left', 'w': 'up', 'd': 'right', 's': 'down'}
    while True:
        # 移动
        dir_key = str(raw_input(': '))
        if dir_key == 'q':
            break
        elif dir_key not in dir_map:
            continue
        direction = dir_map.get(dir_key, None)
        g.move(direction)
        # 刷新图
        g.refresh()
        # 刷新空位
        g.refresh_blank()
        if not g.blank_arr:
            break
        # 空位新生
        g.new_rand()
        # 刷新图
        g.refresh()


if __name__ == '__main__':
    main()

'''
bug1：假设行 2 4 4 4，向左(a)键后，2 8 8，行 2 2 2 2，后为4 4 4，列亦 √
bug2：新生最大值不超过当前表格中的最大值，不太合理，应优化 √
bug3：方向键替代awsd 较好
bug4：当不能再朝着一个方向移动时，应不新生值
bug5：似乎，2 0 0 2，左后 2 0 2 0，未
bug6：列16 2 16 16，下后 0 0 32 32 √ 去除 if tmp and tmp == self.array[i][y]: 后的 else，直接赋值
'''
