def is_valid(color, graph, colors, region):
    for neighbor in graph[region]:
        if colors.get(neighbor) == color:
            return False
    return True


def map_coloring(graph, color_list, colors, regions):
    if not regions:
        return True

    region = regions[0]

    for color in color_list:
        if is_valid(color, graph, colors, region):
            colors[region] = color

            if map_coloring(graph, color_list, colors, regions[1:]):
                return True

            del colors[region]

    return False

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

color_list = ['Red', 'Green', 'Blue']
colors = {}
regions = list(graph.keys())

if map_coloring(graph, color_list, colors, regions):
    print("Map Coloring Solution:")
    for region, color in colors.items():
        print(region, ":", color)
else:
    print("No solution exists.")
