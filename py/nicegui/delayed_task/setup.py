from nicegui import ui

# Making cookies takes time
cookies = 0

ui.label().bind_text_from(globals(), 'cookies', lambda x: f'{x} cookies')
ui.linear_progress().classes('w-1/4')
ui.button('make cookie')

ui.run()
