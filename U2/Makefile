# file names without extension
HS_FILE = haskell
JAVA_FILE = Greet

all: haskell java

haskell: bin/$(HS_FILE)

bin/$(HS_FILE): src/$(HS_FILE).hs
	@mkdir bin
	ghc src/$(HS_FILE).hs -o bin/$(HS_FILE)
	# @rm haskell/*.o haskell/*.hi

java: bin/$(JAVA_FILE).class

bin/$(JAVA_FILE).class: src/$(JAVA_FILE).java
	javac -d bin src/$(JAVA_FILE).java

.PHONY: clean
clean:
	@rm -rf bin