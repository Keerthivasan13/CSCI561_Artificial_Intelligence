import timeit
from collections import deque
import heapq


class Node:
    def __init__(self, coord, parent, path_cost, f_cost):
        self.coord = coord
        self.parent = parent
        self.path_cost = path_cost
        self.f_cost = f_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost


class Node_:
    def __init__(self, coord, parent, path_cost):
        self.coord = coord
        self.parent = parent
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost


class Solution:
    def __main__(self):
        with open("input8.txt", 'r') as file:
            algorithm = file.readline().rstrip()
            # print "Algorithm is " + algorithm
            dim = tuple(map(int, file.readline().split()))
            # print "Columns {} Rows {} ".format(dim[0], dim[1])
            landing_site = tuple(map(int, file.readline().split()))
            # print "Landing Site Coordinates {} {}".format(landing_site[0], landing_site[1])
            thresh = int(file.readline())
            # print "Threshold is {}".format(thresh)
            no_of_targets = int(file.readline())
            targets = []
            # print "No of Targets : {}".format(no_of_targets)
            # print "Targets are "
            for _ in range(no_of_targets):
                targets.append(tuple(map(int, file.readline().split())))
                # print "{} {}".format(targets[-1][0], targets[-1][1])
            # print "Elevations ="
            elevations = []
            for line in file:
                elevations.append(tuple(map(int, line.split())))
                # print elevations[-1]

        output = []
        if algorithm == "BFS":
            output = self.BFS(dim, landing_site, thresh, no_of_targets, targets, elevations)
        elif algorithm == "UCS":
            output = self.UCS(dim, landing_site, thresh, no_of_targets, targets, elevations)
        elif algorithm == "A*":
            output = self.AStar(dim, landing_site, thresh, no_of_targets, targets, elevations)

        with open("output.txt", 'w') as file:
            for target_line in range(no_of_targets):
                if output[target_line]:
                    file.write(
                        " ".join(
                            str(a) + ',' + str(b) for a, b in [entry for entry in [r for r in output[target_line]]]))
                    file.write("\n")
                else:
                    file.write("FAIL\n")
            return

    def BFS(self, dim, landing_site, thresh, no_of_targets, targets, elevations):
        solution = [[]] * no_of_targets
        remaining_targets = list(targets)
        movements = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))
        marked = [[[False] + [-1] * 2] * dim[0] for _ in range(dim[1])]
        to_visit = deque()
        to_visit.append(landing_site)
        marked[landing_site[1]][landing_site[0]] = [True, landing_site]
        while len(to_visit) > 0:
            cur_grid = to_visit.popleft()
            if cur_grid in remaining_targets:
                remaining_targets.remove(cur_grid)
                tracker = cur_grid
                test_case = [tracker]
                while tracker is not landing_site:
                    tracker = marked[tracker[1]][tracker[0]][1]  # Backtracking to the Landing site
                    test_case.append(tracker)
                target_index = targets.index(cur_grid)
                test_case.reverse()
                solution[target_index] = test_case
                if remaining_targets is None:
                    break
            for move in movements:
                new_grid = (cur_grid[0] + move[0], cur_grid[1] + move[1])
                if 0 <= new_grid[0] < dim[0] and 0 <= new_grid[1] < dim[1]:
                    if marked[new_grid[1]][new_grid[0]][0] is False \
                            and abs(elevations[new_grid[1]][new_grid[0]] - elevations[cur_grid[1]][cur_grid[0]]) <= thresh:
                        marked[new_grid[1]][new_grid[0]] = [True, cur_grid]
                        to_visit.append(new_grid)
        return solution

    def UCS(self, dim, landing_site, thresh, no_of_targets, targets, elevations):
        solution = [[]] * no_of_targets
        remaining_targets = list(targets)
        movements = (((0, -1), 10), ((1, -1), 14), ((1, 0), 10), ((1, 1), 14), ((0, 1), 10), ((-1, 1), 14), ((-1, 0), 10), ((-1, -1), 14))
        search_space = []
        path_cost_dict = {}
        heapq.heappush(search_space, Node_(landing_site, None, 0))
        path_cost_dict[landing_site] = 0
        while len(search_space) > 0:
            cur_node = heapq.heappop(search_space)
            if cur_node.path_cost == path_cost_dict[cur_node.coord]:
                if cur_node.coord in remaining_targets:
                    print(cur_node.path_cost)
                    remaining_targets.remove(cur_node.coord)
                    tracker = cur_node
                    test_case = [tracker.coord]
                    while tracker.parent is not None:
                        tracker = tracker.parent
                        test_case.append(tracker.coord)
                    test_case.reverse()
                    target_index = targets.index(cur_node.coord)
                    solution[target_index] = test_case
                    if remaining_targets is None:
                        break
                for move in movements:
                    child_node_coord = (cur_node.coord[0] + move[0][0], cur_node.coord[1] + move[0][1])
                    if 0 <= child_node_coord[0] < dim[0] and 0 <= child_node_coord[1] < dim[1]:
                        if abs(elevations[child_node_coord[1]][child_node_coord[0]] - elevations[cur_node.coord[1]][cur_node.coord[0]]) <= thresh:
                            path_cost = cur_node.path_cost + move[1]
                            if child_node_coord not in path_cost_dict or path_cost_dict[child_node_coord] > path_cost:
                                path_cost_dict[child_node_coord] = path_cost
                                child_node = Node_(child_node_coord, cur_node, path_cost)
                                heapq.heappush(search_space, child_node)
        return solution

    def AStar(self, dim, landing_site, thresh, no_of_targets, targets, elevations):
        solution = [[]] * no_of_targets
        movements = (((0, -1), 10), ((1, -1), 14), ((1, 0), 10), ((1, 1), 14), ((0, 1), 10), ((-1, 1), 14), ((-1, 0), 10),
        ((-1, -1), 14))
        search_space = []
        f_cost_dict = {}
        for t_index in range(len(targets)):
            f_value = self.heuristic(landing_site, targets[t_index])
            heapq.heappush(search_space, Node(landing_site, None, 0, f_value))
            f_cost_dict[landing_site] = f_value
            while len(search_space) > 0:
                cur_node = heapq.heappop(search_space)
                if cur_node.f_cost == f_cost_dict[cur_node.coord]:
                    if cur_node.coord == targets[t_index]:
                        print(cur_node.path_cost)
                        tracker = cur_node
                        test_case = [tracker.coord]
                        while tracker.parent is not None:
                            tracker = tracker.parent
                            test_case.append(tracker.coord)
                        test_case.reverse()
                        solution[t_index] = test_case
                        break
                    for move in movements:
                        child_node_coord = (cur_node.coord[0] + move[0][0], cur_node.coord[1] + move[0][1])
                        if 0 <= child_node_coord[0] < dim[0] and 0 <= child_node_coord[1] < dim[1]:
                            elev_diff = abs(elevations[child_node_coord[1]][child_node_coord[0]] - elevations[cur_node.coord[1]][cur_node.coord[0]])
                            if elev_diff <= thresh:
                                path_cost = cur_node.path_cost + move[1] + elev_diff
                                f_cost = path_cost + self.heuristic(child_node_coord, targets[t_index])
                                if child_node_coord not in f_cost_dict or f_cost_dict[child_node_coord] > f_cost:
                                    f_cost_dict[child_node_coord] = f_cost
                                    heapq.heappush(search_space, Node(child_node_coord, cur_node, path_cost, f_cost))
            search_space.clear()
            f_cost_dict.clear()
        return solution

    def heuristic(self, node, goal):
        dx = abs(node[0] - goal[0])
        dy = abs(node[1] - goal[1])
        return 10 * (dx + dy) + (14 - 2 * 10) * min(dx, dy)

#start_time = time.time()
start = timeit.default_timer()
obj = Solution()
obj.__main__()
print("--- %s seconds ---" % (timeit.default_timer() - start))