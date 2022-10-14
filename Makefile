MAIN	:=	./src/main.py
OS 		:=	$(shell uname -s | tr A-Z a-z)

.PHONY: compile
compile:
ifeq ($(OS),darwin) # MacOS.
	pyinstaller --onefile --distpath ./out --name lpm $(MAIN)
else ifeq ($(OS),linux) # Linux.
	pyinstaller --onefile --distpath ./out --name lpm $(MAIN)
else # Windows.
	@echo "cringe"
endif
