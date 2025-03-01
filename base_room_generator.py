print("{")
print("    \"cells\": [")
width_start, width_stop, height_start, height_stop = -5, 6, -5, 6
for i in range(width_start, width_stop):
    for j in range(height_start, height_stop):
        if i == width_start or i == width_stop-1 or j == height_start or j == height_stop-1:
            print("        {\"position\": [" + str(i) + "," + str(j) + "], \"is_wall\": true},")
        else:
            print("        {\"position\": [" + str(i) + "," + str(j) + "], \"is_wall\": false},")
print("    ]")
print("}")
