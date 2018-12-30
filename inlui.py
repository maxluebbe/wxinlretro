import os
import time
import wx

from  common import Game
import inlrunner
import romdr

SUPPORTED_CONSOLES = ('Gameboy Advance','Nintendo 64', 'Sega Genesis')
CONSOLE_LABEL_TO_FLAG = {'Gameboy Advance': 'gba',
                         'Nintendo 64': 'n64',
                         'Sega Genesis': 'genesis'}

class DumpFrame(wx.Frame):
    def __init__(self, parent, title):
        super(DumpFrame, self).__init__(parent, title=title)
        self.device = inlrunner.INLRunner(dry_run=False)
        self.InitUI()
        self.Centre()

    def on_dump_button(self, event):
        self.dump_button.SetLabel("Dumping...")
        self.dump_button.Disable()
        time.sleep(0.5)
        os.chdir('inlretro_dir/host')
        self.device.dump_rom(CONSOLE_LABEL_TO_FLAG[self.console_input.GetStringSelection()], self.rom_size_input.GetLineText(0).strip())
        while not self.device.is_done():
            time.sleep(1)
        if os.path.exists('dump.bin'):
            os.rename('dump.bin', '../../dump.bin')
        os.chdir('../../')
        if os.path.exists('dump.bin'):
            match = romdr._match_game('dump.bin')
            if match:
                romdr.rename(['dump.bin'])
        
        self.dump_button.SetLabel("Dump")
        self.dump_button.Enable()

    def InitUI(self):
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(3, 2, 9, 25)

        console_text = wx.StaticText(panel, label="Console")
        rom_size_text = wx.StaticText(panel, label="Rom Size (mbit)")

        self.console_input = wx.ComboBox(panel, choices=SUPPORTED_CONSOLES, value=SUPPORTED_CONSOLES[2])
        self.console_input.SetSelection(2)
        self.rom_size_input = wx.TextCtrl(panel)
        self.rom_size_input.write("8")

        self.dump_button = wx.Button(panel, label="Dump")
        self.dump_button.Bind(wx.EVT_BUTTON, self.on_dump_button)

        fgs.AddMany([(console_text), (self.console_input, 1, wx.EXPAND),
                     (rom_size_text), (self.rom_size_input, 1, wx.EXPAND), (self.dump_button, 1, wx.EXPAND)])
           
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)


def main():
    app = wx.App()
    frame = DumpFrame(None, title='wxINLRetro')
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()