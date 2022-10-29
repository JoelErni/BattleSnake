for y in range(11):
        map1 = []
        for x in range(11):
            for snake in game_state['board']['snakes']:
                for body in snake['body']:
                    if body['x'] == x and body['y'] == y:
                        map1.append(1)
                        break
            map1.append(0)
        map.append(map1)

    print(map)