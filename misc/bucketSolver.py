def solve(sizes, target):
    # paths[X] = Y means we went from Y to X
    paths = dict()
    # create a stack for the BFS
    stack = [(0,)*len(sizes)]
    while stack:
        pos = stack.pop(0)
        # did we reach our target? create the path
        if target in pos:
            path = []
            while pos != (0,)*len(sizes):
                path.append(pos)
                pos = paths[pos]
            path.append((0,)*len(sizes))
            print_solution(sizes, path)
            break
        # create all possible new positions by completely filling a bucket
        # and by emptying it
        for i in range(len(sizes)):
            new = pos[:i] + (sizes[i],) + pos[i+1:]
            if new not in paths.keys():
                paths[new] = pos
                stack.append(new)
            new = pos[:i] + (0,) + pos[i+1:]
            if new not in paths.keys():
                paths[new] = pos
                stack.append(new)
        # create all possible new positions by filling a bucket with another one
        for i in range(len(sizes)):
            for j in range(len(sizes)):
                s = pos[i]
                t = pos[j]
                m = sizes[j]
                # if source and target are the same, the source has no water
                # or the target is already filled, nothing new will come
                if i==j or s==0 or t==m:
                    continue
                new = list(pos[::])
                new[i] = max(s-m+t,0)
                new[j] = min(m, t+s)
                new = tuple(new)
                if new not in paths.keys():
                    paths[new] = pos
                    stack.append(new)
                    
    # No solution found
    if not stack:
        print("Found no solution!")
                    
def print_solution(sizes, path):
    # the solution was given backwards, so take that into account
    for i in range(len(path)-1, 0, -1):
        # find what buckets changed to find what was done
        changes = [j for j in range(len(sizes)) if path[i-1][j] != path[i][j]]
        if len(changes) == 1:
            # did we empty it or fill it?
            if path[i-1][changes[0]] == 0:
                explanation = "empty the {} bucket".format(sizes[changes[0]])
            else:
                explanation = "fill the {} bucket".format(sizes[changes[0]])
        else:
            # find the buckets that lost and won water
            l = changes[0] if path[i-1][changes[0]] < path[i][changes[0]] else changes[1]
            w = changes[1] if l == changes[0] else changes[0]
            explanation = "pour the {} bucket into the {} one".format(sizes[l], sizes[w])
        print("{} => {} ({})".format(path[i], path[i-1], explanation))
    print("Done!")
          
# The buckets' capacities in a list
buckets = [3, 5]
# Target value, in the same unit as the buckets' capacities
T = 4
solve(buckets, T)
