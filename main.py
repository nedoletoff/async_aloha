import random
import time


def generate_transmission_time():
    return random.uniform(0, 1)


class User:
    def __init__(self, id, message=None):
        self.id = id
        self.message = message
        self.transmission_attempts = 0

    def transmit_message(self):
        if self.message is not None:
            transmission_time = generate_transmission_time()
            print(f"Пользователь {self.id} передает сообщение в момент времени {transmission_time}")
            if transmission_time < 0.5:
                print(f"Пользователь {self.id} успешно передал сообщение")
                self.message = None
            else:
                print(f"Пользователь {self.id} потерял сообщение в результате столкновения")
                self.transmission_attempts += 1

    def receive_message(self, message):
        print(f"Пользователь {self.id} получил сообщение от пользователя {message.sender_id}")


class System:
    def __init__(self, users):
        self.users = users

    def run(self):
        while True:
            for user in self.users:
                if user.message is not None:
                    user.transmit_message()

            for user in self.users:
                if user.transmission_attempts == 3:
                    print(f"Пользователь {user.id} отказывается от передачи сообщения")
                    user.message = None

            time.sleep(1)


def main():
    users = [User(i, random.randint(0, 100)) for i in range(10)]

    system = System(users)

    system.run()


if __name__ == "__main__":
    main()
