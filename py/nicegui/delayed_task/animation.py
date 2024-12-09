
from nicegui import ui, elements
from typing import Callable, Union, Any

cookies = 0

def delayed_cookie(delay, 
                   callback=Callable[..., Any],
                   progress_element=Union[elements.progress.LinearProgress, elements.progress.CircularProgress, None],
                   ) -> elements.timer.Timer:
    
    def on_complete():
        progress_element.props(f'instant-feedback=0 animation-speed=0')
        progress_element.value = 0
        callback()

    # Delay callback
    t = ui.timer(delay, callback=on_complete, once=True)

    # Change progress element animation to reflect given delay
    if progress_element is not None:
        progress_element.props(f'instant-feedback=0 animation-speed=0')
        progress_element.value = 0
        progress_element.props(f'instant-feedback=0 animation-speed={delay * 1000}')
        progress_element.value = 1
    return t

def make_cookie():
    global cookies
    cookies += 1

ui.label().bind_text_from(globals(), 'cookies', lambda x: f'{x} cookies')
lp = ui.linear_progress(show_value=False).classes('w-1/4')
ui.button('make cookie', on_click=lambda: delayed_cookie(3, callback=make_cookie, progress_element=lp))

ui.run()
