# 6-DoF GraspNet: Variational Grasp Generation for Object Manipulation
Implementation of [6-DoF GraspNet](https://arxiv.org/abs/1905.10520) with tensorflow and python. This repo has been tested with python 2.7 and tensorflow 1.12.


# Как установить и что запускать?

Скачиваем себе на компьютер репозиторий:
```bash
git clone 
```

Переходим в папку:
```bash
cd 6dof-graspnet
```

Собираем пространство:
```bash
conda env create -f graspnet6dof.yml
```

Активируем пространство:
```bash
conda activate graspnet6dof
```
Также необходимо рядом с репозиторием установить pointnet2.
```bash
git clone https://github.com/charlesq34/pointnet2
```



Запускаем генерацию захватов (надо изменить путь до [объекта](./go.stl)):
```bash
python sample.py --num_samples 1000
```

Отображаем сгенерированные на mesh захваты:
```bash
python visualize_gripper.py tmp.json
```

Краткое [описание](./about_sample.txt). [Статья](./text.pdf).