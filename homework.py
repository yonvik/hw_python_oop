from dataclasses import asdict, dataclass, fields
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

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

    SPEED_MULTIPLIER = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        """Расчет каллорий для бега."""
        return (
            (
                self.SPEED_MULTIPLIER
                * self.get_mean_speed()
                - self.SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    FIRST_MULTIPLIER = 0.035
    SECOND_MULTIPLIER = 0.029

    def get_spent_calories(self) -> float:
        """Расчет каллорий для спортивной хотьбы."""
        return (
            (
                self.FIRST_MULTIPLIER
                * self.weight
                + (
                    self.get_mean_speed() ** 2
                    // self.height
                )
                * self.SECOND_MULTIPLIER
                * self.weight
            )
            * self.duration * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: int

    LEN_STEP = 1.38
    MULTIPLIER = 1.1
    SHIFT = 2

    def get_distance(self) -> float:
        """Расчет дистанции для плаванья."""
        return (
            (
                self.action
                * self.LEN_STEP
            )
            / self.M_IN_KM
        )

    def get_mean_speed(self) -> float:
        """Расчет средней скорости для плаванья."""
        return (
            (
                self.length_pool
                * self.count_pool
            )
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Расчет каллорий для плаванья."""
        return (
            (
                (
                    self.get_mean_speed()
                    + self.MULTIPLIER
                )
                * self.SHIFT
            )
            * self.weight
        )


TRAININGS = {
    "SWM": Swimming,
    "RUN": Running,
    "WLK": SportsWalking
}

ERROR_WORKOUT = '{workout_type} не обнаружен.'
ERROR_DATA = 'В тренировке {workout_type} количество параметров: {data}.'


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAININGS:
        raise ValueError(ERROR_WORKOUT.format(workout_type=workout_type))
    if len(data) != len(fields(TRAININGS[workout_type])):
        raise ValueError(ERROR_DATA.format(data=data))
    return TRAININGS.get(workout_type)(*data)


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
