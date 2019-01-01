import os
import time
import wx

from  common import Game
import inlrunner
import romdr

SUPPORTED_CONSOLES = ('Gameboy Advance','Nintendo','Nintendo 64', 'Sega Genesis')
CONSOLE_LABEL_TO_FLAG = {'Gameboy Advance': 'gba',
                         'Nintendo': 'nes',
                         'Nintendo 64': 'n64',
                         'Sega Genesis': 'genesis'}
MAPPER_NAMES = ('bnrom', 'cdream','cninja','cnrom', 'dualport', 'easyNSF', 'fme7', 'mapper30',
                'mmc1', 'mmc3', 'mmc4', 'mmc5', 'nrom', 'unrom')
NES_ROM_SIZES = ('0','16', '32', '64', '128', '256', '512')


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
        if self.console_input.GetStringSelection() != 'Nintendo':
            self.device.dump_rom(CONSOLE_LABEL_TO_FLAG[self.console_input.GetStringSelection()], self.rom_size_input.GetLineText(0).strip())
        else:
            self.device.dump_nes_rom(CONSOLE_LABEL_TO_FLAG[self.console_input.GetStringSelection()],
                                     self.mapper_input.GetStringSelection(), self.prg_rom_input.GetStringSelection(),
                                     self.chr_rom_input.GetStringSelection())
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

    def _disable_controls(self, console):
        if console == 'Nintendo':
            self.mapper_input.Enable()
            self.prg_rom_input.Enable()
            self.chr_rom_input.Enable()
            self.rom_size_input.Disable()
        else:
            self.mapper_input.Disable()
            self.prg_rom_input.Disable()
            self.chr_rom_input.Disable()

    def on_console_change(self, event):
        self._disable_controls(self.console_input.GetStringSelection())
        
    def InitUI(self):
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(6, 2, 9, 25)

        console_text = wx.StaticText(panel, label="Console")
        rom_size_text = wx.StaticText(panel, label="Rom Size (mbit)")
        mapper_text = wx.StaticText(panel, label="Mapper")
        prg_rom_text = wx.StaticText(panel, label="PRG-ROM Size (Kb)")
        chr_rom_text = wx.StaticText(panel, label="CHR-ROM Size (Kb)")

        self.console_input = wx.ComboBox(panel, choices=SUPPORTED_CONSOLES, value=SUPPORTED_CONSOLES[2], style=wx.CB_READONLY)
        self.console_input.SetSelection(2)
        self.console_input.Bind(wx.EVT_COMBOBOX, self.on_console_change)

        self.rom_size_input = wx.TextCtrl(panel)
        self.rom_size_input.write("8")
        
        self.mapper_input = wx.ComboBox(panel, choices=MAPPER_NAMES, value=MAPPER_NAMES[0], style=wx.CB_READONLY)
        self.mapper_input.SetSelection(0)
        self.prg_rom_input = wx.ComboBox(panel, choices=NES_ROM_SIZES, value=NES_ROM_SIZES[4], style=wx.CB_READONLY)
        self.prg_rom_input.SetSelection(4)
        self.chr_rom_input = wx.ComboBox(panel, choices=NES_ROM_SIZES, value=NES_ROM_SIZES[0], style=wx.CB_READONLY)
        self.chr_rom_input.SetSelection(0)

        self.dump_button = wx.Button(panel, label="Dump")
        self.dump_button.Bind(wx.EVT_BUTTON, self.on_dump_button)

        fgs.AddMany([(console_text), (self.console_input, 1, wx.EXPAND),
                     (rom_size_text), (self.rom_size_input, 1, wx.EXPAND),
                     (mapper_text), (self.mapper_input, 1, wx.EXPAND),
                     (prg_rom_text), (self.prg_rom_input, 1, wx.EXPAND),
                     (chr_rom_text), (self.chr_rom_input, 1, wx.EXPAND),
                     (self.dump_button, 1, wx.EXPAND)])
           
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)
        self._disable_controls(self.console_input.GetStringSelection())


def main():
    app = wx.App()
    frame = DumpFrame(None, title='wxINLRetro')
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()