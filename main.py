import flet as ft
import pyautogui, sys, random, asyncio

macro, macro_task = None, None

RANDOM_COMMANDS = []
COMMANDS = []
command_list_view, random_command_list_view = None, None
run_macro_btn, stop_macro_btn, run_btn_container = None, None, None

class CommandItem(ft.Row) :
    def __init__(self, command, command_index) :
        super().__init__()
        
        self.command = command
        self.command_index = command_index
        
        self.command_label = ft.Text(self.command, expand = True)
        self.edit_field = ft.TextField(self.command, hint_text = 'New Command...', expand = True, visible = False, shift_enter = True, on_submit = self.save_callback)
        self.edit_btn = ft.IconButton(icon = 'edit', alignment = ft.alignment.top_right, on_click = self.edit_callback)
        self.save_btn = ft.IconButton(icon = 'save', alignment = ft.alignment.top_right, visible = False, on_click = self.save_callback)
        self.delete_btn = ft.IconButton(icon = 'delete', alignment = ft.alignment.top_right, on_click = self.delete_callback)
        
        self.controls = [
            self.command_label,
            self.edit_field,
            self.edit_btn,
            self.save_btn,
            self.delete_btn
        ]
        self.expand = True
    
    def edit_callback(self, e) :
        global command_list_view
        
        self.command_label.visible = False
        self.edit_btn.visible = False
        
        self.edit_field.visible = True
        self.save_btn.visible = True
        
        self.edit_field.value = self.command
        
        command_list_view.update()
        return
    
    def save_callback(self, e) :
        global command_list_view
        
        self.command = self.edit_field.value
        self.command_label.value = self.command
        
        self.edit_field.visible = False
        self.save_btn.visible = False
        
        self.command_label.visible = True
        self.edit_btn.visible = True
        
        command_list_view.update()
        return
    
    def delete_callback(self, e) :
        global COMMANDS, command_list_view
        
        COMMANDS.pop(self.command_index)
        for i, command in enumerate(COMMANDS) :
            command.command_index = i
            continue
        command_list_view.controls = COMMANDS
        command_list_view.update()
        return

class RandomCommandItem(ft.Row) :
    def __init__(self, random_command, random_command_index) :
        super().__init__()
        
        self.random_command = random_command
        self.random_command_index = random_command_index
        
        self.random_command_label = ft.Text(self.random_command, expand = True)
        self.edit_field = ft.TextField(self.random_command, hint_text = 'New Random Command...', expand = True, visible = False, shift_enter = True, on_submit = self.save_callback)
        self.edit_btn = ft.IconButton(icon = 'edit', alignment = ft.alignment.top_right, on_click = self.edit_callback)
        self.save_btn = ft.IconButton(icon = 'save', alignment = ft.alignment.top_right, visible = False, on_click = self.save_callback)
        self.delete_btn = ft.IconButton(icon = 'delete', alignment = ft.alignment.top_right, on_click = self.delete_callback)
        
        self.controls = [
            self.random_command_label,
            self.edit_field,
            self.edit_btn,
            self.save_btn,
            self.delete_btn
        ]
        self.expand = True
    
    def edit_callback(self, e) :
        global random_command_list_view
        
        self.random_command_label.visible = False
        self.edit_btn.visible = False
        
        self.edit_field.visible = True
        self.save_btn.visible = True
        
        self.edit_field.value = self.random_command
        
        random_command_list_view.update()
        return
    
    def save_callback(self, e) :
        global random_command_list_view
        
        self.random_command = self.edit_field.value
        self.random_command_label.value = self.random_command
        
        self.edit_field.visible = False
        self.save_btn.visible = False
        
        self.random_command_label.visible = True
        self.edit_btn.visible = True
        
        random_command_list_view.update()
        return
    
    def delete_callback(self, e) :
        global RANDOM_COMMANDS, random_command_list_view
        
        RANDOM_COMMANDS.pop(self.random_command_index)
        for i, random_command in enumerate(COMMANDS) :
            random_command.random_command_index = i
            continue
        random_command_list_view.controls = RANDOM_COMMANDS
        random_command_list_view.update()
        return

def add_command(command_name) :
    global COMMANDS, command_list_view
    
    COMMANDS.append(CommandItem(command_name, len(COMMANDS.copy())))
    command_list_view.controls = COMMANDS
    command_list_view.update()
    return

def add_random_command(command_name) :
    global RANDOM_COMMANDS, random_command_list_view
    
    RANDOM_COMMANDS.append(RandomCommandItem(command_name, len(RANDOM_COMMANDS.copy())))
    random_command_list_view.controls = RANDOM_COMMANDS
    random_command_list_view.update()
    return

class Macro() :
    def __init__(self, commands, random_commands, cooldown_time, failsafe_mouse_distance, random_cmd_probability) :
        self._COMMANDS = commands
        self._RANDOM_COMMANDS = random_commands
        self._COOLDOWN_TIME = cooldown_time
        self._FAILSAFE_MOUSE_DISTANCE = failsafe_mouse_distance
        self._RANDOM_COMMAND_PROBABILITY = random_cmd_probability
    
        self.calc_distance = lambda a, b : (((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2)) ** 0.5
        self.failsafe = False
        self.mouse_pos = pyautogui.position()
        return
    
    async def check_failsafe(self) :
        self.failsafe = self.calc_distance(pyautogui.position(), self.mouse_pos) >= self._FAILSAFE_MOUSE_DISTANCE
        self.mouse_pos = pyautogui.position()
        try :
            location = pyautogui.locateOnScreen('assets/owo_dm.png', confidence = 0.7)
            if location :
                self.failsafe = True
        except :
            self.failsafe = False
        if self.failsafe : sys.exit()
        return self.failsafe
    
    async def execute_random_command(self) :
        if random.random() < (self._RANDOM_COMMAND_PROBABILITY / 100.0) :
            await self.execute_command(random.choice(self._RANDOM_COMMANDS), True)
            await asyncio.sleep(1)
        return
    
    async def execute_command(self, cmd, is_random = False) :
        await self.check_failsafe()
        
        pyautogui.write(cmd, interval = random.uniform(0.25, 1.5))
        await self.check_failsafe()
        pyautogui.press('enter')
        
        await self.check_failsafe()
        
        if not is_random :
            await self.execute_random_command()
        return
    
    async def macro_task(self) :
        global run_macro_btn, stop_macro_btn, run_btn_container
        
        try :
            mid_index = len(self._COMMANDS) // 2
            
            first_half = self._COMMANDS[ : mid_index]
            second_half = self._COMMANDS[mid_index : ]
            
            await asyncio.sleep(self._COOLDOWN_TIME)
            self.mouse_pos = pyautogui.position()
            while not self.failsafe :
                await self.check_failsafe()
                
                for cmd in first_half :
                    await self.execute_command(cmd)
                
                
                chance = random.randint(1, 5)
                if chance == 5 :
                    await asyncio.sleep(10)
                
                
                for cmd in second_half :
                    await self.execute_command(cmd)
                
                await asyncio.sleep(random.randint(15, 20))
                await self.check_failsafe()
                continue
        except pyautogui.FailSafeException :
            print('Failsafe mechanism triggered.')
            stop_macro_btn.visible = False
            run_macro_btn.visible = True
            
            run_btn_container.update()
            
            self.failsafe = True
        return

def main(page: ft.Page):
    global COMMANDS, RANDOM_COMMANDS, command_list_view, random_command_list_view, run_macro_btn, stop_macro_btn, run_btn_container
    
    page.title = 'Owo Bot Macro'
    
    light_theme = ft.Theme(color_scheme_seed = ft.Colors.AMBER)
    dark_theme = ft.Theme(color_scheme_seed = ft.Colors.DEEP_ORANGE)
    
    page.theme = light_theme
    page.dark_theme = dark_theme
    
    page.theme_mode = ft.ThemeMode.LIGHT
    
    page.window.center()
    page.window.width = 1000
    page.window.height = 850
    page.window.icon = '/icon.png'
    page.update()
    
    def change_theme(e) :
        if page.theme_mode == ft.ThemeMode.LIGHT :
            theme_switch.thumb_icon = 'dark_mode'
            page.theme_mode = ft.ThemeMode.DARK
        elif page.theme_mode == ft.ThemeMode.DARK :
            theme_switch.thumb_icon = 'light_mode'
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()
        return
    
    theme_switch = ft.Switch(thumb_icon = 'light_mode', on_change = change_theme)
    
    title_area = ft.Column([
        ft.Text('Owo Bot Macro', size = 32, weight = ft.FontWeight.BOLD, style = ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE), expand = True),
        ft.Text('~ By @typedecker', expand = True)
    ], expand = True)
    header_area = ft.Row([
        ft.Image(src = 'icon.png', width = 70, height = 70, border_radius = ft.border_radius.all(70)),
        title_area,
        theme_switch
    ], expand = True)
    title_container = ft.Container(
        header_area,
        width = 1000,
        # height = 100,
        margin = ft.Margin(10, 10, 10, 10),
        padding = ft.Padding(5, 5, 5, 5),
        alignment = ft.alignment.top_left
    )
    
    def add_btn_callback(e) :
        add_cmd_btn.visible = False
        
        add_cmd_field.value = ''
        
        add_cmd_field.visible = True
        add_cmd_done_btn.visible = True
        
        command_area.update()
        return
    
    def done_btn_callback(e) :
        global COMMANDS
        
        add_command(add_cmd_field.value)
        
        add_cmd_field.visible = False
        add_cmd_done_btn.visible = False
        
        add_cmd_btn.visible = True
        
        command_list_view.update()
        command_area.update()
        return
    
    command_area_title_label = ft.Text('Commands (In-Order)', size = 18, weight = ft.FontWeight.BOLD, expand = True)
    add_cmd_field = ft.TextField(label = 'Add Command', expand = True, visible = False, shift_enter = True, on_submit = done_btn_callback)
    add_cmd_done_btn = ft.IconButton(icon = 'done', alignment = ft.alignment.top_right, visible = False, on_click = done_btn_callback)
    add_cmd_btn = ft.IconButton(icon = 'add', alignment = ft.alignment.top_right, on_click = add_btn_callback)
    command_list_view = ft.ListView(COMMANDS, spacing = 5, padding = 10, expand = True)
    command_area = ft.Column([
        ft.Row([
            command_area_title_label,
            add_cmd_field,
            add_cmd_done_btn,
            add_cmd_btn
        ]),
        ft.Divider(),
        command_list_view
    ])
    command_list_container = ft.Container(
        command_area,
        width = 400,
        height = 400,
        margin = ft.Margin(10, 10, 10, 10),
        padding = ft.Padding(5, 5, 5, 5),
        border = ft.border.all(1, ft.Colors.OUTLINE)
    )
    
    def random_add_btn_callback(e) :
        add_random_cmd_btn.visible = False
        
        add_random_cmd_field.value = ''
        
        add_random_cmd_field.visible = True
        add_random_cmd_done_btn.visible = True
        
        random_command_area.update()
        return
    
    def random_done_btn_callback(e) :
        global RANDOM_COMMANDS
        
        add_random_command(add_random_cmd_field.value)
        
        add_random_cmd_field.visible = False
        add_random_cmd_done_btn.visible = False
        
        add_random_cmd_btn.visible = True
        
        random_command_list_view.update()
        random_command_area.update()
        return
    
    random_command_area_title_label = ft.Text('Random Commands', size = 18, weight = ft.FontWeight.BOLD, expand = True)
    add_random_cmd_field = ft.TextField(label = 'Add Random Command', expand = True, visible = False, shift_enter = True, on_submit = random_done_btn_callback)
    add_random_cmd_done_btn = ft.IconButton(icon = 'done', alignment = ft.alignment.top_right, visible = False, on_click = random_done_btn_callback)
    add_random_cmd_btn = ft.IconButton(icon = 'add', alignment = ft.alignment.top_right, on_click = random_add_btn_callback)
    random_command_list_view = ft.ListView(COMMANDS, spacing = 5, padding = 10, expand = True)
    random_command_area = ft.Column([
        ft.Row([
            random_command_area_title_label,
            add_random_cmd_field,
            add_random_cmd_done_btn,
            add_random_cmd_btn
        ]),
        ft.Divider(),
        random_command_list_view
    ])
    random_command_list_container = ft.Container(
        random_command_area,
        width = 400,
        height = 400,
        margin = ft.Margin(10, 10, 10, 10),
        padding = ft.Padding(5, 5, 5, 5),
        border = ft.border.all(1, ft.Colors.OUTLINE)
    )
    
    
    list_area = ft.Row([
        command_list_container,
        random_command_list_container
    ], width = 1000)
    
    
    cooldown_time_slider = ft.Slider(5, min = 1, max = 20, divisions = 20, label = '{value}s', expand = True)
    failsafe_mouse_dist_slider = ft.Slider(100, min = 20, max = 150, divisions = 130, label = '{value}px', expand = True)
    random_cmd_probab_slider = ft.Slider(40, min = 0, max = 100, divisions = 100, label = '{value}%', expand = True)
    
    
    options_area = ft.Column([
        ft.Row([
            ft.Text('Cooldown Time: ', weight = ft.FontWeight.BOLD, style = ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE), expand = True),
            # ft.Slider(5, min = 1, max = 20, divisions = 20, label = '{value}s', expand = True)
            cooldown_time_slider
        ]),
        ft.Row([
            ft.Text('Failsafe Mouse Distance: ', weight = ft.FontWeight.BOLD, style = ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE), expand = True),
            # ft.Slider(100, min = 20, max = 150, divisions = 130, label = '{value}px', expand = True)
            failsafe_mouse_dist_slider
        ]),
        ft.Row([
            ft.Text('Random Command Probability: ', weight = ft.FontWeight.BOLD, style = ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE), expand = True),
            # ft.Slider(40, min = 0, max = 100, divisions = 100, label = '{value}%', expand = True)
            random_cmd_probab_slider
        ])
    ])
    options_container = ft.Container(
        options_area,
        width = 400,
        margin = ft.Margin(10, 10, 10, 10),
        padding = ft.Padding(5, 5, 5, 5),
        border = ft.border.all(1, ft.Colors.OUTLINE)
    )
    
    
    def run_macro_callback(e) :
        global macro, run_macro_btn, stop_macro_btn, run_btn_container, macro_task
        
        _COMMANDS = [cmd.command for cmd in COMMANDS]
        _RANDOM_COMMANDS = [cmd.random_command for cmd in RANDOM_COMMANDS]
        _COOLDOWN_TIME = cooldown_time_slider.value
        _FAILSAFE_MOUSE_DIST = failsafe_mouse_dist_slider.value
        _RANDOM_COMMAND_PROBAB = random_cmd_probab_slider.value
        
        macro = Macro(
            _COMMANDS,
            _RANDOM_COMMANDS,
            _COOLDOWN_TIME,
            _FAILSAFE_MOUSE_DIST,
            _RANDOM_COMMAND_PROBAB
        )
        macro_task = page.run_task(macro.macro_task)
        
        stop_macro_btn.visible = True
        run_macro_btn.visible = False
        run_btn_container.update()
        return
    
    def stop_macro_callback(e) :
        global macro, run_macro_btn, stop_macro_btn, run_btn_container, macro_task
        
        stop_macro_btn.visible = False
        run_macro_btn.visible = True
        run_btn_container.update()
        
        macro.failsafe = True
        macro_task.cancel()
        
        screen_width = pyautogui.size()[0]
        pyautogui.moveTo(screen_width, 0, 1)
        return
    
    run_macro_btn = ft.FilledButton(text = 'Run Macro', icon = 'play_arrow', width = 120, on_click = run_macro_callback)
    stop_macro_btn = ft.FilledButton(text = 'Stop Macro', icon = 'stop_circle', width = 120, visible = False, on_click = stop_macro_callback)
    
    run_btn_container = ft.Container(
        ft.Row([
            run_macro_btn,
            stop_macro_btn
        ], width = 140),
        alignment = ft.alignment.bottom_right
    )
    
    page.add(
        title_container,
        # command_list_container,
        list_area,
        options_container,
        run_btn_container
    )
    
    for cmd_name in ['owo b', 'owo h', 'owo sac all', 'owo upgrade duration all'] :
        add_command(cmd_name)
    
    for cmd_name in ['owo z', 'owo cf 1', 'owo s 1', 'owo cash', 'owo lb all', 'owo wc all', 'owo ws', 'owo tm', 'owo inv'] :
        add_random_command(cmd_name)


ft.app(main, assets_dir="assets")
