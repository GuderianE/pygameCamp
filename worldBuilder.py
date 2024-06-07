

def buildWorldMatrix(width, height, blocks):
    world_map = [[-1 for _ in range(width)] for _ in range(height)]
    
    # Place each block in its specified coordinates
    for block, x, y in blocks:
        if 0 <= x < width and 0 <= y < height:
            world_map[y][x] = block
        
        
    
    return world_map

def blockPlacer(type, x, y):
    