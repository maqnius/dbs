# file names without extension
HS_FILE = haskell
JAVA_FILE = Greet

all: haskell java

haskell: haskell/bin/$(HS_FILE)

haskell/bin/$(HS_FILE): haskell/$(HS_FILE).hs
	@mkdir haskell/bin
	ghc haskell/$(HS_FILE).hs -o haskell/bin/$(HS_FILE)
	@rm haskell/*.o haskell/*.hi

java: java/$(JAVA_FILE).class

java/$(JAVA_FILE).class: java/$(JAVA_FILE).java
	javac java/$(JAVA_FILE).java

.PHONY: clean
clean:
	@rm -rf haskell/bin
	@rm -rf java/*.class