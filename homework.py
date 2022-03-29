from dataclasses import asdict, dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    alert = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.alert.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__qualname__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    Average_speed_run_1 = 18
    Average_speed_run_2 = 20
    Minutes_in_hour = 60

    def get_spent_calories(self) -> float:
        """Расчет каллорий для бега."""
        return (
            (self.Average_speed_run_1 * self.get_mean_speed()
             - self.Average_speed_run_2) * self.weight
            / self.M_IN_KM * self.duration * self.Minutes_in_hour
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    Average_speed_spw_1 = 0.035
    Average_speed_spw_2 = 0.029
    Minutes_in_hour = 60

    def get_spent_calories(self) -> float:
        """Расчет каллорий для спортивной хотьбы."""
        return (
            (self.Average_speed_spw_1 * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.Average_speed_spw_2
             * self.weight) * self.duration * self.Minutes_in_hour
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: int

    LEN_STEP = 1.38
    Average_speed_swm_1 = 1.1
    Average_speed_swm_2 = 2

    def get_distance(self) -> float:
        """Расчет дистанции для плаванья."""
        return ((self.action * self.LEN_STEP) / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Расчет средней скорости для плаванья."""
        return (
            (self.length_pool * self.count_pool)
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Расчет каллорий для плаванья."""
        return (
            ((self.get_mean_speed() + self.Average_speed_swm_1)
             * self.Average_speed_swm_2) * self.weight
        )


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary_training = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type == 'RUN' and len(data) == 3:
        return dictionary_training['RUN'](*data)
    elif workout_type == 'SWM' and len(data) == 5:
        return dictionary_training['SWM'](*data)
    elif workout_type == 'WLK' and len(data) == 4:
        return dictionary_training['WLK'](*data)
    else:
        return('Ошибка, некоректные данные')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
