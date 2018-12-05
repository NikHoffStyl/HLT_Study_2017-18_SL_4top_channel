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
$ nsMain.py
```
which imports histoMaker and adds HistogramMaker() as an argument to the postProcessor. The choice of triggers is given here, along with the preselection criteria.

To produce trigger efficiency plots run:
```
$ python triggerPathEfficiency.py
```

I will try to introduce the option to input a trigger as an argument to some of these and if argument is not given it will revert to search for a default trigger and exit if trigger does not exist.


