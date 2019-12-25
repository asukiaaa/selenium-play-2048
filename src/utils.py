from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from typing import List, TypeVar, Type, Dict


go_delay_second = 0.1


def is_same_boad_cells(boad1, boad2):
    for x in range(4):
        for y in range(4):
            if (boad1[y][x] != boad2[y][x]):
                return False
    return True


def create_key_from_actions(actions: List[str]):
    key = ''
    for action in actions:
        if key != '':
            key += '_'
        key += action
    return key


CellValue = TypeVar('CellType', int, str, None)
RowCells = List[CellValue]
BoadCells = List[RowCells]

class Boad:
    def __init__(self, cells: BoadCells):
        self.cells = cells
        self.boads_after: Dict[str, Type[Boad]] = {}
        self.rotated_clockwize_cells = None

    def is_same(self, boad) -> bool:
        return is_same_boad_cells(boad.cells, self.cells)

    def load_or_create_rotated_clockwize_cells(self) -> BoadCells:
        cells = self.rotated_clockwize_cells
        if cells is not None:
            return cells
        cells = create_cells_rotated_clockwize(self.cells)
        self.rotated_clockwize_cells = cells
        return cells

    def is_jointable_by_up(self) -> bool:
        cells = self.load_or_create_rotated_clockwize_cells()
        for y in range(4):
            if row_has_jointable_cells(cells[y]):
                return True
        return False

    def is_movable_up(self) -> bool:
        return is_movable_left_cells(self.load_or_create_rotated_clockwize_cells())

    def is_movable_right(self) -> bool:
        return is_movable_right_cells(self.cells)

    def is_movable_left(self) -> bool:
        return is_movable_left_cells(self.cells)

    def is_movable_down(self) -> bool:
        return is_movable_right_cells(self.load_or_create_rotated_clockwize_cells())

    def load_or_create_boad_after_action(self, action: str):
        if action in self.boads_after:
            return self.boads_after[action]
        cells = None
        if action == 'left':
            cells = create_cells_after_left(self.cells)
        elif action == 'right':
            cells = create_cells_after_right(self.cells)
        elif action == 'up':
            cells = create_cells_rotated_counter_clockwize(
                create_cells_after_left(self.load_or_create_rotated_clockwize_cells()))
        elif action == 'down':
            cells = create_cells_rotated_counter_clockwize(
                create_cells_after_right(self.load_or_create_rotated_clockwize_cells()))
        self.boads_after[action] = cells
        return Boad(cells)

    def load_or_create_boad_after_actions(self, actions: List[str]):
        key = create_key_from_actions(actions)
        if key in self.boads_after:
            return self.boads_after[key]
        before_actions = actions.copy()
        before_action = before_actions.pop()
        before_boad = self if len(
            before_actions) == 0 else self.load_or_create_boad_after_actions(before_actions)
        boad = before_boad.load_or_create_boad_after_action(before_action)
        self.boads_after[key] = boad
        return boad


def go_right(browser, delay_second=go_delay_second):
    actions = ActionChains(browser)
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()
    sleep(delay_second)


def go_left(browser, delay_second=go_delay_second):
    actions = ActionChains(browser)
    actions.send_keys(Keys.ARROW_LEFT)
    actions.perform()
    sleep(delay_second)


def go_up(browser, delay_second=go_delay_second):
    actions = ActionChains(browser)
    actions.send_keys(Keys.ARROW_UP)
    actions.perform()
    sleep(delay_second)


def go_down(browser, delay_second=go_delay_second):
    actions = ActionChains(browser)
    actions.send_keys(Keys.ARROW_DOWN)
    actions.perform()
    sleep(delay_second)


def read_number_of_cell(browser, x: int, y: int):
    cell_class = "tile-position-{}-{}".format(y+1, x+1)
    cell_elems = browser.find_elements_by_class_name(cell_class)
    elems_len = len(cell_elems)
    if elems_len == 0:
        return None
    elif elems_len == 1:
        text = cell_elems[0].find_element_by_class_name('tile-inner').text
        return int(text)
    else:
        # TODO able to improve
        text = cell_elems[elems_len -
                          1].find_element_by_class_name('tile-inner').text
        return int(text)


def read_boad_cells(browser):
    boad_cells = []
    for x in range(4):
        row_cells = []
        for y in range(4):
            try:
                row_cells.append(read_number_of_cell(browser, x, y))
            except Exception as e:
                print('caused error try again', x, y, e)
                row_cells.append(read_number_of_cell(browser, x, y))
        boad_cells.append(row_cells)
    return boad_cells


def read_to_create_boad(browser):
    cells = read_boad_cells(browser)
    return Boad(cells)


def is_movable_left_cells(cells: BoadCells) -> bool:
    for y in range(4):
        if is_movable_left_row(cells[y]):
            return True
    return False


def is_movable_right_cells(cells: BoadCells) -> bool:
    for y in range(4):
        if is_movable_right_row(cells[y]):
            return True
    return False


def is_movable_horizontal_row(row_cells: RowCells):
    return row_has_cell(row_cells) and (row_has_jointable_cells(row_cells) or row_has_none(row_cells))


def is_movable_right_row(row_cells: RowCells):
    if row_has_jointable_cells(row_cells):
        return True
    prev_cell_index = None
    for x in range(4):
        cell = row_cells[x]
        if cell is None:
            if prev_cell_index is not None:
                return True
        else:
            prev_cell_index = x
    return False


def is_movable_left_row(row_cells: RowCells):
    if row_has_jointable_cells(row_cells):
        return True
    prev_none_index = None
    for x in range(4):
        cell = row_cells[x]
        if cell is not None:
            if prev_none_index is not None:
                return True
        else:
            prev_none_index = x
    return False


def row_has_jointable_cells(row_cells: RowCells) -> bool:
    before_cell = None
    for x in range(4):
        c = row_cells[x]
        if c is not None:
            if before_cell == c:
                return True
            before_cell = c
    return False


def row_has_cell(row_cells: RowCells) -> bool:
    for x in range(4):
        if row_cells[x] is not None:
            return True
    return False


def row_has_none(row_cells: RowCells) -> bool:
    for x in range(4):
        if row_cells[x] is None:
            return True
    return False


def there_are_cell_to_fill_row_none(cells: BoadCells, row_index: int):
    for x in range(4):
        if cells[row_index][x]is None:
            for y in range(4):
                if y > row_index and (cells)[y][x] is not None:
                    return True
    return False


def is_fixed_row(row_cells: RowCells):
    for x in range(3):
        left = row_cells[x]
        right = row_cells[x+1]
        if left == right or left is None:
            return False
    return True


def create_row_cells_after_left(row_cells: RowCells) -> RowCells:
    new_cells = []
    merged_indexes = []
    for cell in row_cells:
        if cell is None:
            continue
        new_cell_len = len(new_cells)
        if new_cell_len == 0:
            new_cells.append(cell)
        elif cell == new_cells[-1] and not new_cell_len-1 in merged_indexes:
            new_cells[new_cell_len-1] += cell
            merged_indexes.append(new_cell_len-1)
        else:
            new_cells.append(cell)
    while len(new_cells) < 4:
        new_cells.append(None)
        # new_cells.append('2or4')
    return new_cells


def create_row_cells_after_right(row_cells: RowCells) -> RowCells:
    reversed_cells = row_cells.copy()
    reversed_cells.reverse()
    reversed_left_cells = create_row_cells_after_left(reversed_cells)
    reversed_left_cells.reverse()
    return reversed_left_cells


def create_cells_rotated_clockwize(cells: BoadCells) -> BoadCells:
    rotated_cells = []
    for y in range(4):
        row = []
        for x in range(4):
            row.append(cells[3-x][y])
        rotated_cells.append(row)
    return rotated_cells


def create_cells_rotated_counter_clockwize(cells: BoadCells) -> BoadCells:
    rotated_cells = []
    for y in range(4):
        row = []
        for x in range(4):
            row.append(cells[x][3-y])
        rotated_cells.append(row)
    return rotated_cells


def create_cells_after_left(cells: BoadCells) -> BoadCells:
    new_cells = []
    for y in range(4):
        new_cells.append(create_row_cells_after_left(cells[y]))
    return new_cells


def create_cells_after_right(cells: BoadCells) -> BoadCells:
    new_cells = []
    for y in range(4):
        new_cells.append(create_row_cells_after_right(cells[y]))
    return new_cells


def create_cells_after_up(cells: BoadCells):
    rotated_cells = create_cells_rotated_counter_clockwize(cells)
    rotated_then_left_cells = create_cells_after_left(rotated_cells)
    return create_cells_rotated_clockwize(rotated_then_left_cells)


def jointable_by_left_up(cells: RowCells, upper_row_index: int):
    after_left_cells = create_cells_after_left(cells)
    for x in range(3):
        upper = after_left_cells[upper_row_index][x]
        lower = after_left_cells[upper_row_index+1][x]
        if upper == lower and upper is not None:
            return True
    return False


def is_row_keeps_larger_right(row_cells: RowCells) -> bool:
    left = row_cells[0]
    right_index = 1
    while right_index < len(row_cells):
        right = row_cells[right_index]
        print('left right', left, right)
        if left is not None and right is not None and left >= right:
            return False
        if right is not None:
            left = right
        right_index += 1
    return True


def get_mininum_cell_in_row(row_cells: RowCells) -> int or None:
    min_cell = None
    for x in range(4):
        c = row_cells[x]
        if c is None:
            continue
        if min_cell is None or c < min_cell:
            min_cell = c
    return min_cell


def get_better_direction_to_joint(cells: BoadCells, focused_row_index: int) -> List[str]:
    after_cells = {
        'right': create_cells_after_right(cells),
        # 'left': create_cells_after_left(cells),
        'up': create_cells_after_up(cells),
    }
    if is_row_keeps_larger_right(after_cells['right'][0]):
        return 'right'
    elif is_row_keeps_larger_right(after_cells['up'][0]):
        return 'up'
    min_cell = {
        'right': get_mininum_cell_in_row(after_cells['right'][0]),
        'up': get_mininum_cell_in_row(after_cells['up'][0]),
    }
    if min_cell['right'] is None and min_cell['up'] is None:
        raise 'consider'
        return 'up'
    elif min_cell['right'] is None or min_cell['up'] is None:
        if min_cell['right'] is None:
            return 'up'
        else:
            return 'right'
    else:
        if min_cell['right'] < min_cell['up']:
            return 'up'
        else:
            return 'right'
    print(after_cells)


def handle_for_row(browser, boad, target_row_index: int) -> bool:
    cells = boad.cells
    if is_movable_right_row(cells[target_row_index]):
        print('right because top is not filled')
        go_right(browser)
    # DONE 右上に小さい駒が入っていたら、そちらに注力したい
    # TODO その消したい駒より大きいものが存在するなら、まずそれを消したい
    elif (
        not boad.is_jointable_by_up()
        and is_fixed_row(cells[target_row_index])
        and jointable_by_left_up(cells, target_row_index)
        # and is_row_keeps_larger_right(cells[target_row_index])
    ):
        print('up left to joint left upper')
        go_left(browser)
        go_up(browser)
    elif row_has_none(cells[target_row_index]) and there_are_cell_to_fill_row_none(cells, target_row_index):
        print('up to fill top none')
        go_up(browser)
    elif boad.is_jointable_by_up() and row_has_jointable_cells(cells[target_row_index]):
        dir = get_better_direction_to_joint(cells, target_row_index)
        print('dir', dir)
        if dir == 'right':
            print('go right because better than up')
            go_right(browser)
        else:
            print('go up because better than up')
            go_up(browser)
    elif boad.is_jointable_by_up():
        print('up because jointable upper')
        go_up(browser)
    elif row_has_jointable_cells(cells[target_row_index]):
        print('right because top have jointable cells')
        go_right(browser)
    else:
        return False
    return True
