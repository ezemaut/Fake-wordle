from cx_Freeze import setup, Executable

#Run in consoloe:
# python setup.py build

setup(
    name="Worlde?",
    version="1.0",
    description="Add your own words and audios!",
    options={"build_exe": {"include_files": ["audios/", "Guessing_words.txt","Icon.ico"]}},
    executables=[Executable("FakeWorlde.py", base="Win32GUI", icon=r"Icon.ico")],
)

