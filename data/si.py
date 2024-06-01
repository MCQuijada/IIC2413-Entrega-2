lineas1 = ['Pablo O Ryan', 'Pablo.ORyan@bbdduc.utopia', '56942']
lineas2 = ['270623', 'HKUQYNXP23', 'Av. OHiggins 456, Rancagua', '6101']

print(lineas1+lineas2)
largo = len(lineas1)
print(largo)

lineas2[0] = lineas1[largo-1]+lineas2[0]
print(lineas2)

linea = [elem1 + elem2 for elem1, elem2 in zip(lineas1, lineas2)]
print(linea)