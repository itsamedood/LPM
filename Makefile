MAIN=src/main.py
GUI=src/gui.py
DISTPATH=bin
GUI_DISTPATH=$(DISTPATH)/gui
EXEC=lpm
GUI_EXEC=LPM
PYI_FLAGS=--onefile

both:
	pyinstaller --onefile --distpath $(DISTPATH) --name $(EXEC) $(MAIN)
	pyinstaller --onefile --distpath $(GUI_DISTPATH) --name $(GUI_EXEC) $(GUI)
	@echo "Done."

cmd:
	pyinstaller --onefile --distpath $(DISTPATH) --name $(EXEC) $(MAIN)
	@echo "Done."
	@lpm

gui:
	pyinstaller --onefile --distpath $(GUI_DISTPATH) --name $(GUI_EXEC) $(GUI)
	@echo "Done."
	@./bin/gui/LPM
