from typing import Dict, List


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    training_type = ' '

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        mean_speed: float = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    training_type = 'Running'

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """Наследуем Родительский класс."""
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Расчет каллорий для бега"""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        midl_speed: float = self.get_mean_speed()
        spent_calories: float = ((coeff_calorie_1 * midl_speed
                                 - coeff_calorie_2) * self.weight
                                 / self.M_IN_KM) * (self.duration * 60)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = 'SportsWalking'

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет каллорий для спортивной хотьбы."""
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        mean_speed: float = self.get_mean_speed()
        spent_calories: float = (coeff_calorie_1 * self.weight + (mean_speed**2
                                 // self.height)
                                 * coeff_calorie_2
                                 * self.weight) * (self.duration * 60)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    training_type = 'Swimming'
    LEN_STEP = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Расчет дистанции для плаванья."""
        return ((self.action * self.LEN_STEP) / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Расчет средней скорости для плаванья."""
        mean_speed: float = ((self.length_pool
                             * self.count_pool)
                             / self.M_IN_KM) / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Расчет каллорий для плаванья."""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        mean_speed: float = self.get_mean_speed()
        spent_calories: float = (((mean_speed + coeff_calorie_1)
                                  * coeff_calorie_2) * self.weight)
        return spent_calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    code: Dict[str, int] = {"SWM": Swimming,
                            "RUN": Running,
                            "WLK": SportsWalking}
    action, duration, weight, *other = data
    return code.get(workout_type)(action, duration, weight, *other)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
