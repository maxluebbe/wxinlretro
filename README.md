## wxinlretro
A portable Desktop UI for inlretro based on wxwidgets!

## License
MIT License

Copyright (c) 2018 Max Luebbe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Dependencies
- Python 3
- wxpython (Python 3)
- inlretro host application

## Setup
- Install wxpython via pip (haven't gotten it working with virtualenv)

  - ```$ pip3 install wxpython```

- Download source for [inlretro](https://gitlab.com/InfiniteNesLives/INL-retro-progdump), follow instructions there to build it.
- Create a directory called inlretro_dir local to wxinlretro root directory. From inlretro, copy the shared and host directories there.
- If you are using Windows, edit inlrunner.py to refer to the correct binary for your platform. (I have only tested on OS X/Linux, this should work, let me know if it doesn't!)

  - ```BIN = 'inlretro.exe'```

## Usage
To run the application:

 ```$ python3 inlui.py```

Watch stdout for helpful messages, because they aren't displayed in the UI itself (yet)

Functionality is pretty limited right now:
 - Backing up and identifying GBA cartridges.
 - Backing up and identifying NES cartridges in headerless format.
 - Backing up and identifying N64 cartridges.
 - Backing up and identifying Sega Genesis cartridges.

## Getting Help
- Some issues will be due to current state of the inlretro application, and what systems and functionality are currently supported via its command-line interface. ALWAYS MAKE SURE YOU HAVE A RECENT VERSION OF THE HOST APPLICATION!
- Make sure your cartridges are clean, and try a different cartridge. I suspect that there are variants that are not handled correctly by the host application at this time? If you found a bug or problem with the host application that is being used by the UI, [file an issue for inlretro on gitlab](https://gitlab.com/InfiniteNesLives/INL-retro-progdump/issues).
- If you're stuck or found a bug, [file an issue](https://github.com/maxluebbe/wxinlretro/issues) here on github.