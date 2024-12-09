from abc import ABC, abstractmethod
from nicegui import ui
from typing import Callable, Any

_tick_list = []
_current_tick = 0
TPS = 20 # Ticks per second

class Tickable(ABC):
    @abstractmethod
    def tick(self, current_tick):
        pass

# A basic timer used in conjunction with tick system
class Timer(Tickable):
    def __init__(self,
                 duration,
                 callback=Callable[..., Any]):
        
        self.callback = callback
        self.duration = duration

        self.elapsed = 0
        self.percent_complete = 0
        self._complete = True

    def tick(self, current_tick):
        if not self._complete:
            if self.percent_complete >= 1:
                self._complete = True
                self.elapsed = self.duration
                self.percent_complete = 1
                self.callback()
            else:  
                self.elapsed += 1 / TPS
                self.percent_complete = self.elapsed / self.duration

    def reset(self):
        if self._complete:
            self.elapsed = 0
            self.percent_complete = 0
            self._complete = False


def provide_ticks_to(*args: Tickable | Callable[[int], Any]):
    _tick_list.extend(args)

# Call tick for everything added to _tick_list
def _tick():
    global _current_tick, _tick_list
    for x in _tick_list:   
        if isinstance(x, Tickable):
            x.tick(_current_tick)
        else:
            x(_current_tick)
    _current_tick += 1

def start_game_ticks():
    # Constantly call _tick
    ui.timer(1 / TPS, callback=_tick)

# ---

def make_cookie():
    global cookies
    cookies += 1

cookies = 0

timer = Timer(3, callback=make_cookie)
provide_ticks_to(timer)
start_game_ticks()

ui.label().bind_text_from(globals(), 'cookies', lambda x: f'{x} cookies')
ui.linear_progress(show_value=False)\
    .bind_value_from(globals()['timer'], 'percent_complete')\
    .classes('w-1/4')\
    .props('animation-speed=150')

ui.label().bind_text_from(globals()['timer'], 'elapsed', lambda s: f'{round(s, 1)}s')
ui.button('make cookie', on_click=lambda: timer.reset())

ui.run()
