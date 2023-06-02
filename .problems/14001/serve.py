base_cnt, animal_cnt, gun_length = list(map(int, input().split(" ")))  # 첫번째 입력

bases = list(map(int, input().split(" ")))  # 두번째 입력 (base_cnt개)

animals = []
for i in range(animal_cnt):
    animals.append(list(map(int, input().split(" "))))  # 세번째 ~ m+2번째 입력
