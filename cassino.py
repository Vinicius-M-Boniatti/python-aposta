from abc import ABC, abstractmethod
import itertools
import random
import os
from time import sleep

# Definição da classe base abstrata
class BaseMachine(ABC):
    @abstractmethod
    def _get_final_result(self):
        pass

    @abstractmethod
    def _display(self, amount_bet, result, time=0.05):
        pass

    @abstractmethod
    def _emojize(self, emojis):
        pass

    @abstractmethod
    def _check_result_user(self, result):
        pass

    @abstractmethod
    def _update_balance(self, amount_bet, result, player):
        pass

    @abstractmethod
    def play(self, amount_bet, player):
        pass

# Classe do jogador
class Player:
    def __init__(self, balance=0):
        self.balance = balance

# Classe da máquina caça-níquel
class CassaNiquel(BaseMachine):
    def __init__(self, level=1, balance=0):
        self.SIMBOLOS = {
            'money_mouth_face': '1F911',
            'money_bag': '1F4B0',
            'money_with_wings': '1F4B8',
            'dollar_banknote': '1F4B5',
            'coin': '1FA99'
        }
        self.level = level
        self.permutations = self._gen_permutations()
        self.balance = balance

    def _gen_permutations(self):
        permutations = list(itertools.product(self.SIMBOLOS.keys(), repeat=3))
        for _ in range(self.level):
            for i in self.SIMBOLOS.keys():
                permutations.append((i, i, i))
        return permutations

    def _get_final_result(self):
        if not hasattr(self, 'permutations'):
            self.permutations = self._gen_permutations()

        result = list(random.choice(self.permutations))

        if len(set(result)) == 3 and random.uniform(0, 5) >= 2:
            result[1] = result[0]

        return result

    def _display(self, amount_bet, result, time=0.05):
        seconds = 2
        print("🎰 Girando... 🎰")
        for _ in range(int(seconds / time)):
            temp_result = random.choice(self.permutations)
            print(self._emojize(temp_result), end="\r")
            sleep(time)
            os.system('cls')
            
        print("\n🎰 Resultado final:", self._emojize(result))

        if self._check_result_user(result):
            premio = amount_bet * 3
            print(f"🎉 VOCÊ GANHOU: {premio} moedas! 🎉")
        else:
            print("❌ VOCÊ PERDEU ❌")

    def _emojize(self, emojis):
        return " | ".join(chr(int(self.SIMBOLOS[code], 16)) for code in emojis)

    def _check_result_user(self, result):
        return all(x == result[0] for x in result)

    def _update_balance(self, amount_bet, result, player: Player):
        if self._check_result_user(result):
            self.balance -= (amount_bet * 3)
            player.balance += (amount_bet * 3)
        else:
            self.balance += amount_bet
            player.balance -= amount_bet

    def play(self, amount_bet, player: Player):
        if player.balance < amount_bet:
            print("❌ Saldo insuficiente! ❌")
            return

        result = self._get_final_result()
        self._display(amount_bet, result)
        self._update_balance(amount_bet, result, player)

# Exemplo de uso
maquina1 = CassaNiquel(level=4, balance=5000)  # Define um saldo para a máquina
player1 = Player(1000)  # Define um saldo inicial para o jogador
maquina1.play(10, player1)  # O jogador aposta 10 moedas
print(f"Saldo final do jogador: {player1.balance} moedas")



# for _ in range(10):
#     maquina1.play(10, player1)  # O jogador aposta 10 moedas

# print(f"Saldo final do jogador: {player1.balance} moedas")
