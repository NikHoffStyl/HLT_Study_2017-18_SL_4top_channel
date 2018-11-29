# Remote Work
Repository for Working in the Single Lepton tttt decay channel

To produce a text file of triggers( and other unwanted stuff, which will be removed) do:
```
$ HLTnames.py | tee LeafNames.txt
```
or
```
$ HLTnames.py > LeafNames.txt
```

To produce histograms run:
```
$ python histoMaker.py
```

To produce trigger efficiency plots run:
```
$ python triggerPathEfficiency.py
```

I will try to introduce the option to input a file as an argument to some of these and if argument is not given it will revert to search for a default file and exit if file does not exist.


