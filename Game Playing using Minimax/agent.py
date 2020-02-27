import time
class Node:
    def __init__(self, depth, best_move):
        self.depth = depth
        self.best_move = best_move

class Solution:
    def __main__(self):
        with open("input.txt", 'r') as file:
            self.board = []
            # Read the inputs from the file
            self.play_type = file.readline().rstrip()
            self.maximizing_pawn_color = file.readline()[0]
            self.time_remaining = float(file.readline())
            self.start_time = time.time()
            self.max_time = self.time_remaining + time.time() - 5  # 10 secs
            for _ in range(16):
                self.board.append(list(file.readline().rstrip()))

            # Initialize useful variables
            if self.maximizing_pawn_color == 'B':
                self.minimizing_pawn_color = 'W'
            else:
                self.minimizing_pawn_color = 'B'

            self.movements = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

            self.black_camp = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                               (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                               (0, 2), (1, 2), (2, 2), (3, 2),
                               (0, 3), (1, 3), (2, 3),
                               (0, 4), (1, 4)}
            self.white_camp = {(15, 15), (14, 15), (13, 15), (12, 15), (11, 15),
                               (15, 14), (14, 14), (13, 14), (12, 14), (11, 14),
                               (15, 13), (14, 13), (13, 13), (12, 13),
                               (15, 12), (14, 12), (13, 12),
                               (15, 11), (14, 11)}

            self.source = {'W': self.white_camp, 'B': self.black_camp}
            self.target = {'B': self.white_camp, 'W': self.black_camp}
            self.base_corner = {'B': (0, 0), 'W': (15, 15)}

            self.starting_position = (0, 0)

            self.max_pawns = set()
            self.min_pawns = set()
            for row in range(16):
                for col in range(16):
                    if self.board[row][col] == self.maximizing_pawn_color:
                        self.max_pawns.add((col, row))
                    elif self.board[row][col] == self.minimizing_pawn_color:
                        self.min_pawns.add((col, row))

            node = Node(0, [])

            if self.game_playing_agent(node) != -1:
                with open("output.txt", 'w') as file:
                    source, moves = node.best_move

                    if abs(source[0] - moves[0][0]) > 1 or abs(source[1] - moves[0][1]) > 1:
                        does_jump = True
                    else:
                        does_jump = False

                    for move in moves:
                        if does_jump:
                            file.write("J ")
                        else:
                            file.write("E ")
                        file.write("{},{} {},{}".format(source[0], source[1], move[0], move[1]))
                        file.write("\n")
                        source = move
            return

    def game_playing_agent(self, node):
        if self.play_type == "SINGLE":
            pawns_at_camp = self.source[self.maximizing_pawn_color].intersection(self.max_pawns)

            if len(pawns_at_camp):
                entire_move_list = {}
                for pawn_coord in pawns_at_camp:
                    entire_move_list.setdefault(pawn_coord, []).extend(
                        self.get_valid_moves(pawn_coord, self.maximizing_pawn_color))

                    for valid_move in entire_move_list[pawn_coord]:
                        if valid_move[-1] not in self.source[self.maximizing_pawn_color]:
                            node.best_move = [pawn_coord, valid_move]
                            return

                for pawn_coord, valid_moves in entire_move_list.items():
                    for valid_move in valid_moves:
                        if self.further_away_check(self.maximizing_pawn_color, pawn_coord, valid_move[-1]):
                            node.best_move = [pawn_coord, valid_move]
                            return

            for pawn_coord in self.max_pawns - pawns_at_camp:
                move = self.get_valid_move_single(pawn_coord, self.maximizing_pawn_color)
                if len(move) != 0:
                    node.best_move = [pawn_coord, move]
                    return

        else:
            max_near_target = 0
            min_near_target = 0
            if self.maximizing_pawn_color == 'W':
                for row in range(8):
                    for col in range(8):
                        if self.board[row][col] == 'W':
                            max_near_target += 1

                for row in range(8, 16):
                    for col in range(8, 16):
                        if self.board[row][col] == 'B':
                            min_near_target += 1
            else:
                for row in range(8, 16):
                    for col in range(8, 16):
                        if self.board[row][col] == 'B':
                            max_near_target += 1
                for row in range(8):
                    for col in range(8):
                        if self.board[row][col] == 'W':
                            min_near_target += 1

            # Default Depth is 2
            self.allowed_depth = 2
            if (min_near_target > 17 or max_near_target > 17) and self.time_remaining > 100:
                self.allowed_depth = 3

            if self.time_remaining < 40:
                self.allowed_depth = 1
            elif self.time_remaining < 100:
                self.allowed_depth = 2

            self.mini_max(node, float('-Inf'), float('Inf'), True)

            if not node.best_move:
                return -1

    def mini_max(self, node, alpha, beta, maximizing_player):
        if node.depth >= self.allowed_depth or self.max_time < time.time() or self.terminal_state_check():
            return self.utility_function()

        if maximizing_player:
            max_value = float('-Inf')
            pawns_at_camp = self.source[self.maximizing_pawn_color].intersection(self.max_pawns)

            if len(pawns_at_camp):
                entire_move_list = {}
                preferred_moves = {}
                for pawn_coord in pawns_at_camp:
                    entire_move_list.setdefault(pawn_coord, []).extend(
                        self.get_valid_moves(pawn_coord, self.maximizing_pawn_color))

                for pawn_coord, valid_moves in entire_move_list.items():
                    for valid_move in valid_moves:
                        if valid_move[-1] not in self.source[self.maximizing_pawn_color]:
                            preferred_moves.setdefault(pawn_coord, []).append(valid_move)

                if len(preferred_moves) == 0:
                    for pawn_coord, valid_moves in entire_move_list.items():
                        for valid_move in valid_moves:
                            if self.further_away_check(self.maximizing_pawn_color, pawn_coord, valid_move[-1]):
                                preferred_moves.setdefault(pawn_coord, []).append(valid_move)

                if len(preferred_moves):
                    self.allowed_depth = 3
                    for pawn_coord, valid_moves in preferred_moves.items():
                        for valid_move in valid_moves:
                            target = valid_move[-1]
                            self.update_board(pawn_coord, target)
                            self.max_pawns.remove(pawn_coord)
                            self.max_pawns.add(target)
                            child_node = Node(node.depth + 1, [])
                            value = self.mini_max(child_node, alpha, beta, False)
                            self.max_pawns.add(pawn_coord)
                            self.max_pawns.remove(target)
                            self.update_board(target, pawn_coord)
                            if value > max_value:
                                max_value = value
                                node.best_move = [pawn_coord, valid_move]
                                alpha = max(alpha, max_value)
                                if alpha >= beta or self.time_remaining < 20:
                                    return max_value
                    return max_value

            pawn_list = []
            for col in range(16):
                for row in range(16):
                    if self.board[row][col] == self.maximizing_pawn_color and (col, row) not in pawns_at_camp:
                        pawn_list.append((col, row))
            if self.maximizing_pawn_color == 'W':
                pawn_list = pawn_list[::-1]

            # Check for valid moves for each child of node compute max value
            for pawn_coord in pawn_list: #self.max_pawns - pawns_at_camp:
                for valid_move in self.get_valid_moves(pawn_coord, self.maximizing_pawn_color):
                    if (time.time() - self.start_time > 15):
                        self.allowed_depth = 2
                    target = valid_move[-1]
                    self.update_board(pawn_coord, target)
                    self.max_pawns.remove(pawn_coord)
                    self.max_pawns.add(target)
                    child_node = Node(node.depth + 1, [])
                    value = self.mini_max(child_node, alpha, beta, False)
                    self.max_pawns.add(pawn_coord)
                    self.max_pawns.remove(target)
                    self.update_board(target, pawn_coord)

                    if value > max_value:
                        max_value = value
                        node.best_move = [pawn_coord, valid_move]
                        alpha = max(alpha, max_value)
                        if alpha >= beta or self.time_remaining < 20:
                            return max_value
            return max_value
        else:
            min_value = float('Inf')
            pawns_at_camp = self.source[self.minimizing_pawn_color].intersection(self.min_pawns)

            if len(pawns_at_camp):
                entire_move_list = {}
                preferred_moves = {}
                for pawn_coord in pawns_at_camp:
                    entire_move_list.setdefault(pawn_coord, []).extend(
                        self.get_valid_moves(pawn_coord, self.minimizing_pawn_color))

                for pawn_coord, valid_moves in entire_move_list.items():
                    for valid_move in valid_moves:
                        if valid_move[-1] not in self.source[self.minimizing_pawn_color]:
                            preferred_moves.setdefault(pawn_coord, []).append(valid_move)

                if len(preferred_moves) == 0:
                    for pawn_coord, valid_moves in entire_move_list.items():
                        for valid_move in valid_moves:
                            if self.further_away_check(self.minimizing_pawn_color, pawn_coord, valid_move[-1]):
                                preferred_moves.setdefault(pawn_coord, []).append(valid_move)

                if len(preferred_moves):
                    for pawn_coord, valid_moves in preferred_moves.items():
                        for valid_move in valid_moves:
                            target = valid_move[-1]

                            self.update_board(pawn_coord, target)
                            self.min_pawns.remove(pawn_coord)
                            self.min_pawns.add(target)
                            child_node = Node(node.depth + 1, [])
                            value = self.mini_max(child_node, alpha, beta, True)
                            self.min_pawns.remove(target)
                            self.min_pawns.add(pawn_coord)
                            self.update_board(target, pawn_coord)

                            if value < min_value:
                                min_value = value
                                node.best_move = [pawn_coord, valid_move]
                                beta = min(beta, min_value)
                                if alpha >= beta or self.time_remaining < 20:
                                    return min_value
                    return min_value

            pawn_list = []
            for col in range(16):
                for row in range(16):
                    if self.board[row][col] == self.minimizing_pawn_color and (col, row) not in pawns_at_camp:
                        pawn_list.append((col, row))
            if self.minimizing_pawn_color == 'W':
                pawn_list = pawn_list[::-1]

            # Check for valid moves for each child of node compute max value
            for pawn_coord in pawn_list: #self.min_pawns - pawns_at_camp:
                for valid_move in self.get_valid_moves(pawn_coord, self.minimizing_pawn_color):
                    target = valid_move[-1]

                    self.update_board(pawn_coord, target)
                    self.min_pawns.remove(pawn_coord)
                    self.min_pawns.add(target)
                    child_node = Node(node.depth + 1, [])
                    value = self.mini_max(child_node, alpha, beta, True)
                    self.min_pawns.remove(target)
                    self.min_pawns.add(pawn_coord)
                    self.update_board(target, pawn_coord)

                    if value < min_value:
                        min_value = value
                        node.best_move = [pawn_coord, valid_move]
                        beta = min(beta, min_value)
                        if alpha >= beta or self.time_remaining < 20:
                            return min_value
            return min_value

    def get_valid_moves(self, cur_pos, pawn_color):
        valid_moves = []
        visited_path = [cur_pos]

        self.starting_position = cur_pos
        valid_moves.extend(self.get_jump_steps(cur_pos, pawn_color, visited_path))

        for move in self.movements:  # self.single_movements[pawn_color]:
            new_pos = (cur_pos[0] + move[0], cur_pos[1] + move[1])
            # Check for the move's validity
            if self.do_validity_test(cur_pos, new_pos, pawn_color) and self.board[new_pos[1]][new_pos[0]] == '.':
                valid_moves.append([new_pos])
        return valid_moves

    def get_jump_steps(self, cur_pos, pawn_color, visited_path):
        valid_jumps = []
        for move in self.movements:
            skip_pawn = (cur_pos[0] + move[0], cur_pos[1] + move[1])
            # Check for the move's validity
            if 0 <= skip_pawn[0] < 16 and 0 <= skip_pawn[1] < 16 and self.board[skip_pawn[1]][skip_pawn[0]] != '.':
                new_pos = (skip_pawn[0] + move[0], skip_pawn[1] + move[1])
                if 0 <= new_pos[0] < 16 and 0 <= new_pos[1] < 16 and self.board[new_pos[1]][new_pos[0]] == '.':
                    if new_pos not in visited_path:
                        visited_path.append(new_pos)
                        for jump in self.get_jump_steps(new_pos, pawn_color, visited_path):
                            valid_jumps.insert(0, [new_pos])
                            for x in jump:
                                valid_jumps[0].append(x)

                        if not ((self.starting_position in self.target[pawn_color] and new_pos not in self.target[
                            pawn_color])
                                or (self.starting_position not in self.source[pawn_color] and new_pos in self.source[
                                    pawn_color])):
                            valid_jumps.insert(-1, [new_pos])
        return valid_jumps
        
    def get_valid_move_single(self, cur_pos, pawn_color):
        valid_moves = []
        visited_path = [cur_pos]

        for move in self.movements:
            new_pos = (cur_pos[0] + move[0], cur_pos[1] + move[1])
            # Check for the move's validity
            if self.do_validity_test(cur_pos, new_pos, pawn_color) and self.board[new_pos[1]][new_pos[0]] == '.':
                valid_moves.append(new_pos)
                return valid_moves

        self.starting_position = cur_pos
        valid_moves.extend(self.get_jump_step_single(cur_pos, pawn_color, visited_path))

        return valid_moves

    def get_jump_step_single(self, cur_pos, pawn_color, visited_path):
        valid_jumps = []
        for move in self.movements:
            skip_pawn = (cur_pos[0] + move[0], cur_pos[1] + move[1])
            # Check for the move's validity
            if 0 <= skip_pawn[0] < 16 and 0 <= skip_pawn[1] < 16 and self.board[skip_pawn[1]][skip_pawn[0]] != '.':
                new_pos = (skip_pawn[0] + move[0], skip_pawn[1] + move[1])
                if 0 <= new_pos[0] < 16 and 0 <= new_pos[1] < 16 and self.board[new_pos[1]][new_pos[0]] == '.':
                    if new_pos not in visited_path:
                        visited_path.append(new_pos)
                        if not ((self.starting_position in self.target[pawn_color] and new_pos not in self.target[
                            pawn_color])
                                or (self.starting_position not in self.source[pawn_color] and new_pos in self.source[
                                    pawn_color])):
                            valid_jumps.append(new_pos)
                            return valid_jumps
                        for jump in self.get_jump_step_single(new_pos, pawn_color, visited_path):
                            valid_jumps.append(new_pos)
                            valid_jumps.append(jump)
                        return valid_jumps
        return valid_jumps

    def do_validity_test(self, cur_pos, new_pos, pawn_color):
        if 0 <= new_pos[0] < 16 and 0 <= new_pos[1] < 16 and \
                (new_pos not in self.source[pawn_color] or cur_pos in self.source[pawn_color]) and \
                (cur_pos not in self.target[pawn_color] or new_pos in self.target[pawn_color]):
            return True
        return False

    def update_board(self, source, target):
        pawn = self.board[source[1]][source[0]]
        self.board[source[1]][source[0]] = self.board[target[1]][target[0]]
        self.board[target[1]][target[0]] = pawn

    def utility_function(self):
        free_max_goals = (self.target[self.maximizing_pawn_color] - (self.max_pawns.union(self.min_pawns)))
        free_min_goals = (self.target[self.minimizing_pawn_color] - (self.max_pawns.union(self.min_pawns)))
        max_score = 0
        min_score = 0

        max_pawns_at_camp = self.max_pawns.intersection(self.source[self.maximizing_pawn_color])
        min_pawns_at_camp = self.min_pawns.intersection(self.source[self.minimizing_pawn_color])
        max_pawns_at_enemy_camp = self.max_pawns.intersection(self.target[self.maximizing_pawn_color])
        min_pawns_at_enemy_camp = self.min_pawns.intersection(self.target[self.minimizing_pawn_color])

        for max_pawn in max_pawns_at_camp.union(max_pawns_at_enemy_camp):
            max_score += self.diagonal_distance(max_pawn, self.base_corner[self.minimizing_pawn_color])

        if len(free_max_goals):
            for max_pawn in self.max_pawns - max_pawns_at_camp - max_pawns_at_enemy_camp:
                distances = [self.diagonal_distance(max_pawn, goal) for goal in free_max_goals]
                max_score += max(distances) + self.diagonal_distance(max_pawn,
                                                                     self.base_corner[self.minimizing_pawn_color])
        if len(min_pawns_at_enemy_camp) > 0:
            for min_pawn in min_pawns_at_camp.union(min_pawns_at_enemy_camp):
                min_score += self.diagonal_distance(min_pawn, self.base_corner[self.maximizing_pawn_color])

            if len(free_min_goals):
                for min_pawn in self.min_pawns - min_pawns_at_camp - min_pawns_at_enemy_camp:
                    distances = [self.diagonal_distance(min_pawn, goal) for goal in free_min_goals]
                    min_score += max(distances) + self.diagonal_distance(min_pawn,
                                                                         self.base_corner[self.maximizing_pawn_color])
        return min_score - max_score

    def diagonal_distance(self, source, target):
        dx = abs(source[0] - target[0])
        dy = abs(source[1] - target[1])
        return dx * dx + dy * dy

    def further_away_check(self, pawn_color, source, target):
        move = [target[0] - source[0], target[1] - source[1]]
        if pawn_color == 'W':
            if move[0] > 0 or move[1] > 0:
                return False
        else:
            if move[0] < 0 or move[1] < 0:
                return False
        return True

    def terminal_state_check(self):
        if (len(self.max_pawns.intersection(self.target[self.maximizing_pawn_color])) == 19 or
                len(self.min_pawns.intersection(self.target[self.minimizing_pawn_color])) == 19):
            return True
        return False

obj = Solution()
obj.__main__()
