import random

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


class Exercise:
    tense_list = ['Präsens (er) ', 'Präteritum (ich) ', 'Perfekt (er) ']
    verb_list = {}

    def __init__(self, verb_file):
        with open(verb_file, 'r') as file:
            for line in file:
                verb, praesens, praeteritum, perfekt = line.strip().split(",")
                self.verb_list[verb] = [praesens, praeteritum, perfekt]

    def get_random_verb(self):
        return random.choice(list(self.verb_list.keys()))


exercise = Exercise('verb_list.csv')


class OpeningWindow(Screen):
    pass


class MainWindow(Screen):

    answer_list = []
    answer1 = ObjectProperty(None)
    answer2 = ObjectProperty(None)
    answer3 = ObjectProperty(None)
    current_verb = ObjectProperty(None)
    next_button = ObjectProperty(None)
    mistake_counter = 0

    def add_answers(self):
        if self.next_button.text == 'weiter':
            self.change_button_text()
        else:
            self.answer_list.clear()
            self.answer_list.append(self.answer1)
            self.answer_list.append(self.answer2)
            self.answer_list.append(self.answer3)
            self.check_current_result()

    def check_current_result(self):
        for i in range(3):
            if self.answer_list[i].text == exercise.verb_list[self.current_verb.text][i]:
                self.answer_list[i].foreground_color = (0, 1, 0, 1)
            else:
                self.answer_list[i].foreground_color = (1, 0, 0, 1)
                self.answer_list[i].text += " > {}".format(exercise.verb_list[self.current_verb.text][i])
                self.mistake_counter += 1
        self.change_button_text()

    def change_button_text(self):
        if self.next_button.text == 'check':
            self.next_button.text = 'weiter'
        else:
            self.reset()

    def reset(self):
        self.next_button.text = 'check'
        self.current_verb.text = exercise.get_random_verb()
        for i in range(3):
            self.answer_list[i].foreground_color = (0, 0, 0, 1)
            self.answer_list[i].text = ""

    def stop(self):
        screen_manager.current = 'result'
        screens[2].get_final_score()


class ResultWindow(Screen):

    final_score = ObjectProperty(None)

    def get_final_score(self):
        self.final_score.text = "Du hast {} Fehler gemacht".format(str(screens[1].mistake_counter))


class WindowManager(ScreenManager):
    pass


class DeutscheVerben(App):

    def build(self):
        return screen_manager


kv_source = Builder.load_file('deutscheverben.kv')

screen_manager = WindowManager()

screens = [OpeningWindow(name="opening"), MainWindow(name="main"), ResultWindow(name="result")]
for screen in screens:
    screen_manager.add_widget(screen)

Window.softinput_mode = 'below_target'

screens[1].current_verb.text = exercise.get_random_verb()

if __name__ == '__main__':
    DeutscheVerben().run()
