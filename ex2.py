prediction = model.predict(x)

n = 0
while n <= 9:
    print(classs[n] + ' = ' + str(prediction[n]))
    n += 1