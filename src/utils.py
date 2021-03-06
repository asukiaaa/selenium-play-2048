from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from typing import List, TypeVar, Type, Dict
import re

CellValue = TypeVar('CellType', int, None)
RowCells = List[CellValue]
BoadCells = List[RowCells]
go_delay_second = 0.1

right_actions = [
    ['right'],
    ['right', 'up'],
    ['right', 'right', 'up'],
    ['right', 'right', 'right', 'up'],
]
left_actions = [
    ['left'],
    ['left', 'up'],
    ['left', 'left', 'up'],
    ['left', 'left', 'left', 'up'],
]
candidate_actions_for_right = [
    ['up'],
] + right_actions + left_actions
candidate_actions_for_left = [
    ['up']
] + left_actions + right_actions


def won_game(browser):
    try:
        browser.find_element_by_css_selector('div.game-message.game-won')
        return True
    except Exception:
        return False


def click_keep_playing_button(browser):
    try:
        browser.find_element_by_css_selector('.keep-playing-button').click()
        return True
    except Exception:
        return False


def is_same_row_cells(row1: RowCells, row2: RowCells):
    for x in range(4):
        if row1[x] != row2[x]:
            return False
    return True


def is_same_boad_cells(boad1: BoadCells, boad2: BoadCells):
    for y in range(4):
        if not is_same_row_cells(boad1[y], boad2[y]):
            return False
    return True


def create_key_from_actions(actions: List[str]):
    key = ''
    for action in actions:
        if key != '':
            key += '_'
        key += action
    return key


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
        return is_movable_right_cells(self.load_or_create_rotated_clockwize_cells())

    def is_movable_right(self) -> bool:
        return is_movable_right_cells(self.cells)

    def is_movable_left(self) -> bool:
        return is_movable_left_cells(self.cells)

    def is_movable_down(self) -> bool:
        return is_movable_left_cells(self.load_or_create_rotated_clockwize_cells())

    def will_change_row_by_actions(self, actions: List[str], row_index: int) -> bool:
        boad = self.load_or_create_boad_after_actions(actions)
        return not is_same_row_cells(boad.cells[row_index], self.cells[row_index])

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
                create_cells_after_right(self.load_or_create_rotated_clockwize_cells()))
        elif action == 'down':
            cells = create_cells_rotated_counter_clockwize(
                create_cells_after_left(self.load_or_create_rotated_clockwize_cells()))
        boad = Boad(cells)
        self.boads_after[action] = boad
        return boad

    def load_or_create_boad_after_actions(self, actions: List[str]):
        key = create_key_from_actions(actions)
        if key in self.boads_after:
            return self.boads_after[key]
        before_actions = actions.copy()
        last_action = before_actions.pop()
        before_boad = self if len(
            before_actions) == 0 else self.load_or_create_boad_after_actions(before_actions)
        boad = before_boad.load_or_create_boad_after_action(last_action)
        self.boads_after[key] = boad
        return boad

    def get_actions_for_row(self, target_row_index: int, direction: str):
        is_direction_right = direction == 'right'
        candidate_actions = candidate_actions_for_right if is_direction_right else candidate_actions_for_left
        current_row = self.cells[target_row_index]
        best_actions_row_points = 0
        best_actions = None
        need_to_keep_larger = is_row_keeps_larger_right(current_row) if is_direction_right else is_row_keeps_larger_left(current_row)
        for actions in candidate_actions:
            boad = self.load_or_create_boad_after_actions(actions)
            row = boad.cells[target_row_index]
            is_row_filled = is_row_filled_right(row) if is_direction_right else is_row_filled_left(row)
            is_row_keeps_larger = is_row_keeps_larger_right(row) if is_direction_right else is_row_keeps_larger_left(row)
            if (
                not is_same_row_cells(current_row, row)
                and (not need_to_keep_larger or is_row_keeps_larger)
                and is_row_filled
            ):
                points = get_row_points(row)
                if points > best_actions_row_points:
                    best_actions_row_points = points
                    best_actions = actions
        return best_actions

    def create_next_by_actions(self, browser, actions: List[str]):
        boad = self
        for action in actions:
            boad_after_action = boad.load_or_create_boad_after_action(action)
            tile_go(browser, action)
            if not boad.is_same(boad_after_action):
                boad = boad_after_action.create_boad_by_read_and_insert_new_tile(
                    browser)
        return boad

    def create_boad_by_read_and_insert_new_tile(self, browser):
        tile = None
        try:
            tile = read_new_tile(browser)
        except Exception:
            tile = read_new_tile(browser)
        # print('tile', tile)
        x = tile['x']
        y = tile['y']
        if self.cells[y][x] is not None:
            raise 'error position for new tile'
        cells = self.cells.copy()
        cells[y][x] = tile['value']
        return Boad(cells)


def tile_go(browser, action):
    actions = ActionChains(browser)
    if action == 'left':
        actions.send_keys(Keys.ARROW_LEFT)
    elif action == 'right':
        actions.send_keys(Keys.ARROW_RIGHT)
    elif action == 'up':
        actions.send_keys(Keys.ARROW_UP)
    elif action == 'down':
        actions.send_keys(Keys.ARROW_DOWN)
    actions.perform()
    sleep(go_delay_second)


def get_row_points(row: RowCells):
    points = 0
    for x in range(4):
        c = row[x]
        if c is not None:
            points += c
    return points


# def get_number_of_cell_from_tile_emenents(elements: [WebElement], x: int, y: int) -> CellValue:
#     cell_class = "tile-position-{}-{}".format(y+1, x+1)
#     target_elements = []
#     for elem in elements:
#         if cell_class in elem.get_attribute('class'):
#             target_elements.append(elem)
#     elem_len = len(target_elements)
#     target_element = None
#     if elem_len == 0:
#         return None
#     elif elem_len == 1:
#         target_element = target_elements[0]
#     else:
#         for elem in target_elements:
#             if 'tile-merged' in elem.get_attribute('class'):
#                 target_element = elem
#                 break
#     text = target_element.find_element_by_class_name('tile-inner').text
#     return int(text)


# def read_boad_cells(browser, retry_count=1):
#     try:
#         boad_cells = []
#         tile_elements = browser.find_elements_by_css_selector(
#             '.tile-container .tile')
#         for x in range(4):
#             row_cells = []
#             for y in range(4):
#                 row_cells.append(
#                     get_number_of_cell_from_tile_emenents(tile_elements, x, y))
#             boad_cells.append(row_cells)
#         return boad_cells
#     except Exception as e:
#         if retry_count > 0:
#             return read_boad_cells(browser, retry_count-1)
#         else:
#             print(e)
#             raise 'cannot read tile numbers'


def read_new_tile(browser):
    elem = browser.find_element_by_css_selector('div.tile.tile-new')
    class_attr = elem.get_attribute('class')
    m = re.search(r"tile-position-([1-4])-([1-4])", class_attr)
    text = elem.find_element_by_class_name('tile-inner').text
    return {
        "value": int(text),
        "x": int(m.group(1)) - 1,
        "y": int(m.group(2)) - 1,
    }


def read_number_of_cell(browser, x: int, y: int):
    cell_class = "tile-position-{}-{}".format(x+1, y+1)
    text = None
    try:
        text = browser.find_element_by_css_selector(
            'div.tile.' + cell_class + '.tile-merged .tile-inner').text
    except Exception:
        try:
            text = browser.find_element_by_css_selector(
                'div.tile.' + cell_class + ' .tile-inner').text
        except Exception:
            return None
    return int(text)


def read_boad_cells(browser):
    boad_cells = []
    for y in range(4):
        row_cells = []
        for x in range(4):
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


def is_row_keeps_larger_left(row_cells: RowCells) -> bool:
    row = row_cells.copy()
    row.reverse()
    return is_row_keeps_larger_right(row)


def is_row_keeps_larger_right(row_cells: RowCells) -> bool:
    left = row_cells[0]
    right_index = 1
    while right_index < len(row_cells):
        right = row_cells[right_index]
        if left is not None and right is not None and left > right:
            return False
        if right is not None:
            left = right
        right_index += 1
    return True


def is_row_filled_left(row_cells: RowCells) -> bool:
    row = row_cells.copy()
    row.reverse()
    return is_row_filled_right(row)


def is_row_filled_right(row_cells: RowCells) -> bool:
    prev_cell = None
    for x in range(4):
        cell = row_cells[x]
        if x != 0 and prev_cell is not None and cell is None:
            return False
        prev_cell = cell
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
