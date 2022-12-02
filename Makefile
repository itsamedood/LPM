MAIN	:=	./src/main.py
OS 		:=	$(shell uname -s | tr A-Z a-z)

.PHONY: all
compile:
ifeq ($(OS),darwin) # MacOS.
# CxFreeze is way faster than PyInstaller on MacOS.
	cxfreeze $(MAIN) --target-dir ./out --target-name lpm
else ifeq ($(OS),linux) # Linux.
	pyinstaller --onefile --distpath ./out --name lpm $(MAIN)
else # Windows.
	@echo "Please help me get LPM working on Windows! I do not currently have access to Windows, thus cannot test LPM nor compile it on Windows."
endif

package:
	cp -R ./out/* ./export
