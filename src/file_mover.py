import os

for file in os.listdir('../history/src/'):
    print(file)
    folder, filename = file.split('_')
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.rename(os.path.join('../history/src/', file), os.path.join(folder, filename))
