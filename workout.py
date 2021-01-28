import numpy as np

def workout_sequence():
    workouts = ['스쿼트', '턱걸이', '푸쉬업', '종아리']
    np.random.shuffle(workouts)
    print(workouts)
    
if __name__ == '__main__':
    workout_sequence()
