import numpy as np
import mpmath as math
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import deque
import csv



# direction definition:
# 0: left 1: right 2: up 3: down

def heuristic2(x,y): # used to find the shortest path between each node
    #y = goals[0]
    return(abs(y[0] - x[0]) + abs(y[1]-x[1]))
    #return ((y[0] - x[0])**2 + (y[1] - x[1])**2)
    # sum = 0
    # for goal in goals:
    #     if goal != [-2,-2]:
    #         sum += (abs(goal[0] - x[0]) + abs(goal[1]-x[1]))
    # return sum

def heuristic(x,goals,csgraph1,maze,visited,unavaiable,rows,columns):
    # return the total length of MST
    import itertools
    import copy
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import minimum_spanning_tree
    allpoints = copy.deepcopy(goals)
    allpoints.append(x)
    #allpoints = [a for a in allpoints if a!= [-2,-2]]
    N = len(allpoints)
    csgraph =   [[0 for x in range(N)] for y in range(N)]
    for first, second in itertools.combinations(allpoints, 2):
        N1 = allpoints.index(first)
        N2 = allpoints.index(second)
        if (first != [-2, -2] and second != [-2, -2]):
            if N2 == N-1:
                #csgraph[N1][N2] = abs(second[0] - first[0]) + abs(second[1]-first[1])
                csgraph[N1][N2] = Astar2(maze,visited,unavaiable,first,second,rows,columns)
            else:
               # print(N1,N2)
                csgraph[N1][N2] = csgraph1[N1][N2]
    tree = minimum_spanning_tree(csgraph)
    tree = tree.toarray().astype(int)

    sum = 0
    for row in range(len(tree)):
        for col in range(len(tree[0])):
            sum = sum + tree[row][col]
    #print("sum" + str(sum))
    return sum






def Astar():
    import read_maze
    import copy
    (csgraph,pairs,costs,paths,maze,visited,unavaiable,start,goals,rows,columns) = setupGraph()
    # set up the problem as a TSP
    points = len(goals)
    print(points)
    print(start,goals)
    # record the previous position of each point
    prev = [[[-1, -1] for x in range(2**points)] for y in range(points+1)]   # record all the history
    #print("prev done")
    collected = '0' * points # collected is a vector that contains which dots have been collected
    #print(collected)
    #collected_int = int(collected,2) # collected_int is the index of what the 3rd dimension value is
    path = []
    steps = 1
    expanded = 0
    cost = 0
    #goal = goals[0]
    #print(goals)
    heu_start = heuristic(start,goals,csgraph,maze,visited,unavaiable,rows,columns)
    print("heu done")
    mincost = [[9999999 for x in range(2**points)] for y in range(points+1)]
    # record the explored set
    print("min done")
    frontier = [[start[0],start[1],heu_start,cost,collected]]
    print("start")
    foundpath = []
    while(len(frontier)!=0):
        node_now = min(frontier, key=lambda t: t[2])
        #print(node_now)
        cost = node_now[3]
        #print(steps)
        frontier.remove(node_now)
        x = node_now[0]
        y = node_now[1]
        #print(x,y)
        collected = node_now[4]
        collected_int = int(collected,2)
        print(collected)
        #visited[x][y][collected_int] = 1
        goal_here = copy.deepcopy(goals)
        #print(goal_here)
        for i in range(points):
            if collected[i] == '1':
                goal_here[i] = [-2,-2]
        if ([x,y] in goal_here):
            i = goal_here.index([x,y])
            collected[i] = '1'
        if collected == '1'*points:
            print("solution found")
            print(expanded)
            print(cost)
            pos_now = [x,y]
            goalnames = ['0','1','2','3','4','5','6','7','8','9']
            goalnames.extend(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t'])
            goalnames.extend(['u','v','w','x','y','z'])
            goalnames.extend(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W'])
            goalnames.extend(['X','Y','Z'])
         #   print(pos_now)
         #   print(collected)
            goalnames = goalnames[:points]
            goalnames.reverse()
            foundpath = []
            idx = goals.index(pos_now)
            goalname = iter(goalnames)
            while collected_int != 0:
                foundpath.append(idx)
                maze[goals[idx][0]][goals[idx][1]] = next(goalname)
                (idx,collected_int) = (prev[idx][collected_int])
            foundpath.reverse()
            maze[start[0]][start[1]] = 'P'
            path.reverse()
            print(path)
            length = len(path)
            print("Total length of the path is " + str(cost))
            print("Number of expanded nodes is " + str(expanded))
            # write it
            with open('test_file.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                for r in maze:
                    r = ''.join(str(word) for word in r)
                    print(r)
                    writer.writerow(r)
            return
        # loop over all possible nodes
        for want in goal_here:
            if want != [-2,-2]:
                idx = goal_here.index(want)
                s = [x,y]
                e = want
                if [s, e] in pairs:
                    pairidx = pairs.index([s, e])

                else:
                    pairidx = pairs.index([e, s])
                cost_now = costs[pairidx]
                cost_temp = cost + cost_now
                collected_temp = copy.deepcopy(collected)
                temp = list(collected_temp)
                temp[idx] = '1'
                collected_temp = "".join(temp)
                collected_int_temp = int(collected_temp,2)
                goal_temp = copy.deepcopy(goal_here)
                goal_temp[idx] = [-2,-2]
                if (cost_temp < mincost[idx][collected_int_temp]): # right
                    mincost[idx][collected_int_temp] = cost_temp
                    heu = heuristic(want,goal_temp,csgraph,maze,visited,unavaiable,rows,columns)
                    if [x,y] == start:
                        prev[idx][collected_int_temp] = [points,collected_int]
                    else:
                        idxhere = goals.index([x,y])
                        prev[idx][collected_int_temp] = [idxhere, collected_int]
                    frontier.append([want[0],want[1],heu+cost_temp,cost_temp,collected_temp])

        expanded += 1

def Astar2(maze,visited,unavaiable,start,goal,rows,columns):

    #print(start,goal)
    prev = [[[-1, -1] for x in range(columns)] for y in range(rows)]  # record all the history
    path = []
    steps = 1
    expanded = 0
    heu_start = heuristic2(start,goal)
    mincost = [[9999999 for x in range(columns)] for y in range(rows)]
    frontier = [[start[0],start[1],heu_start,steps]]
    explored = 0
    while(len(frontier)!=0):
        node_now = min(frontier, key=lambda t: t[2])
        steps = node_now[3]
        #print(steps)
        frontier.remove(node_now)
        x = node_now[0]
        y = node_now[1]
        #visited[x][y] = 1
        if (x == goal[0] and y == goal[1]):
            #print("solution found")
            pos_now = goal
            while (pos_now != start):
                path.append(pos_now)

                pos_now = prev[pos_now[0]][pos_now[1]]
               # maze[pos_now[0]][pos_now[1]] = '.'
            #maze[start[0]][start[1]] = "P"
            path.reverse()
            #print(path)
            length = len(path)
            # print("Total length of the path is " + str(length))
            # print("Number of expanded nodes is " + str(expanded))
            # print("Number of explored nodes is " + str(explored))

            #print(length)
            return(length)
        # loop over all possible nodes
        if (unavaiable[x+1][y] == 0 and (steps+1 < mincost[x+1][y])): # right
            mincost[x+1][y] = steps+1
            heu = heuristic2([x+1,y],goal)
            prev[x+1][y] = [x,y]
            frontier.append([x+1,y,heu+steps+1,steps+1])
            expanded += 1

        if (unavaiable[x-1][y] == 0  and (steps+1 < mincost[x-1][y])): # left
            mincost[x-1][y] = steps+1
            heu = heuristic2([x-1,y],goal)
            prev[x-1][y] = [x,y]
            frontier.append([x-1,y,heu+steps+1,steps+1])
            expanded += 1

        if (unavaiable[x][y-1] == 0 ) and (steps+1 < mincost[x][y-1]): # down
            mincost[x][y-1] = steps+1
            heu = heuristic2([x,y-1],goal)
            prev[x][y-1] = [x,y]
            frontier.append([x,y-1,heu+steps+1,steps+1])
            expanded += 1

        if (unavaiable[x][y+1] == 0 and (steps+1 < mincost[x][y+1])): # up
            mincost[x][y+1] = steps+1
            heu = heuristic2([x,y+1],goal)
            prev[x][y+1] = [x,y]
            frontier.append([x,y+1,heu+steps+1,steps+1])
            expanded += 1
        explored += 1


def setupGraph ():
    import itertools
    import copy
    import read_maze
    import Astar
    maze, visited, unavaiable, start, goal, rows, columns = read_maze.generate_maze()
    goal_temp = copy.deepcopy(goal)
    goal_temp.append(start)
    print(len(goal))
    paths = []
    costs = []
    pair = []
    N = len(goal_temp)
    csgraph = [[0 for x in range(N)] for y in range(N)]

    for first, second in itertools.combinations(goal_temp,2):
        #print("copy")
        #visited1= copy.deepcopy(visited)
        #maze1 = copy.deepcopy(maze)
        #unavaiable1 = copy.deepcopy(unavaiable)
        #print("index")
        N1 = goal_temp.index(first)
        N2 = goal_temp.index(second)
        #print(first)
        #print(second)
        cost = Astar2(maze,visited,unavaiable,first,second,rows,columns)
        #cost = Astar.Astar(maze1, visited1, unavaiable1, first, second, rows, columns)
        csgraph[N1][N2] = cost
        costs.append(cost)
        pair.append([first,second])
    print("graph done")
    print(pair)
    return (csgraph,pair, costs, paths, maze,visited,unavaiable,start,goal,rows,columns)

#def main():
 #  setupGraph()

def main():
    # Astar3()
    Astar()

if __name__ == "__main__":
    main()
