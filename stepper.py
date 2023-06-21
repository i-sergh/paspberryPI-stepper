import RPi.GPIO as GPIO
import time

class Stepper():

    def __init__(self, DIR=20, STEP=21, step_delay=0.002):
        # Пины
        self._DIR = DIR
        self._STEP = STEP

        self._step_delay = step_delay
        # направление движения мотора
        self._direction = True

        self._steps = 0

        # Объявляем генератор
        self._one_step = self._step_generator()

    def setup(self):
        '''
        Подготовка портов
        '''
        # Настраиваем GPIO-пины и режимы управления
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._DIR, GPIO.OUT)
        GPIO.setup(self._STEP, GPIO.OUT)

        # Устанавливаем начальное направление вращения мотора
        self._set_direction()



    def _set_direction(self):
        '''
        Установка направления движения мотора
        '''
        GPIO.output(self._DIR, self._direction)

    def change_direction(self):
        '''
        Меняем направление движения мотора
        '''
        self._direction = not self._direction
        self._set_direction()

    def set_DIR(self, DIR):
        self._DIR = DIR
    
    def set_STEP(self, STEP):
        self._STEP = STEP
    
    def set_step_delay(self, step_delay):
        self._step_delay = step_delay

    def _step_generator(self):
        '''
        Генератор, воспроизводит один шаг движения мотора за вызов
        '''
        for _ in range(self._steps):
            GPIO.output(self._STEP, GPIO.HIGH)
            time.sleep(self._step_delay)
            GPIO.output(self._STEP, GPIO.LOW)
            time.sleep(self._step_delay)
            yield _
    
    def work(self):
        '''
        основной вызов работы мотора
        '''
        try:
            next(self._one_step)
        except StopIteration:
            pass
    
    def set_steps(self, steps):
        self._steps = steps
        self._one_step = self._step_generator()

    def stop(self):
        '''
        Остановка мотора
        '''
        GPIO.output(self._STEP, GPIO.LOW)
        self._steps = 0
    
    def release(self):
        self.stop()
        GPIO.cleanup()