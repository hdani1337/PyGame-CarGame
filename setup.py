import cx_Freeze

executables = [cx_Freeze.Executable("pygame.py")]

cx_Freeze.setup(
    name="Amokfutás v0.1",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["img/car.png", "img/carCrash.png", "img/enemyCar.png", "img/enemyCarCrash.png", "img/bg.png", "img/bg_intro.png", "img/bg_lost.png", "img/bg_opt.png", "img/bg_pause.png"]}},
    executables = executables

    )
