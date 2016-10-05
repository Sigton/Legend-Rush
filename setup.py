import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Legend Rush",
    options={"build_exe": {"packages":["pygame",
                                       "json"],
                           "includes":["blob.py",
                                       "constants.py",
                                       "heart.py",
                                       "imp.py",
                                       "level.py",
                                       "platforms.py",
                                       "player.py",
                                       "spritesheet.py",
                                       "terrain.py",
                                       "tools.py"],
                           "included_files":["level_data",
                                             "resources"]
                           }
             },
    executables=executables
    )
