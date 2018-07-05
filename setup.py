from cx_Freeze import setup, Executable

exe = Executable(
    script="main.py",
    base="Win32GUI",
)

setup(
    name="movieStats",
    version="0.1",
    description="IMDB movie statistics",
    executables=[exe]
)