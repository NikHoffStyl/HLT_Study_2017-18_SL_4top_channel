import ROOT as r


def getMaxY(hists):
    maxYs = []
    for h in (hists):
        if h != None:
            maxYs.append(h.GetMaximum())
    return max(maxYs)


def getSmallestMaxY(hists):
    maxYs = []
    for h in (hists):
        if h != None:
            maxYs.append(h.GetMaximum())
    return min(maxYs)


def getMinMaxX(hists):
    minXs = []
    maxXs = []
    for h in (hists):
        if h != None:
            for i in range(1, h.GetNbinsX()):
                if h.GetBinContent(i) > 0:
                    minXs.append(h.GetBinLowEdge(i))
                    maxXs.append(h.GetBinLowEdge(i) + h.GetBinWidth(i))

    return min(minXs), max(maxXs)


def get2DHists(layers, inputFile, dirName):
    histsPerLayer = {}
    for layer in layers:
        histsPerLayer[layer] = inputFile.Get('{dir}/{hist}'.format(dir=dirName, hist=layer)).Clone()
    return histsPerLayer


def get1DProjections(layers, inputFile, dirName, pu_ranges, normFactor=1, rebinFactor=1):
    projections_perLayer = {}
    hists_2d = get2DHists(layers, inputFile, dirName)

    for counter, layer in enumerate(layers):
        projections_perLayer[layer] = {}
        hist_2d = hists_2d[layer]
        hist_2d.Scale(normFactor)

        for pu_range_counter, pu_range in enumerate(pu_ranges):
            minBin = hist_2d.GetXaxis().FindBin(pu_range[0])
            maxBin = hist_2d.GetXaxis().FindBin(pu_range[-1])
            puRangeLabel = getPURangeLabel(pu_range)
            proj = hist_2d.ProjectionY('name', minBin, maxBin).Clone()

            proj.Rebin(rebinFactor)
            proj.SetLineColor(800 + pu_range_counter)
            proj.SetMarkerColor(800 + pu_range_counter)
            proj.SetMarkerStyle(4)
            projections_perLayer[layer][puRangeLabel] = proj

    return projections_perLayer


def getNumEventsInPURange(inputFile, dirNameNormHist='demo/Clusters/nClusters', minX=0, maxX=50):
    hist = inputFile.Get(dirNameNormHist)
    minXBin = hist.FindBin(minX)
    maxXBin = hist.FindBin(maxX) - 1
    return hist.Integral(minXBin, maxXBin), hist.GetEntries()


def getPURangeLabel(pu_range):
    return '{min}_{max}'.format(min=pu_range[0], max=pu_range[-1])


def normaliseListOfHistsToOne(hists):
    for h in (hists):
        if h != None:
            h.Scale(1 / h.Integral())


def getNumEventsInPURanges(fileNames, pu_ranges):
    nEventsInPURange = {}
    puWeightHists = {}
    for counter, (label, fileName) in enumerate(fileNames.items()):
        inputFile = r.TFile(fileName)

        nEventsInPURange[label] = {}

        puHistName = 'demo/Vertices/nTrueInteractions'
        if label is 'Data': puHistName = 'demo/Vertices/lumiScalers_pu'
        puWeightHists[label] = inputFile.Get(puHistName)
        for pu_range in pu_ranges:
            pu_range_label = getPURangeLabel(pu_range)
            nEventsInPURange[label][pu_range_label], nEntries = getNumEventsInPURange(inputFile,
                                                                                      dirNameNormHist=puHistName,
                                                                                      minX=pu_range[0],
                                                                                      maxX=pu_range[-1])
    return nEventsInPURange, puWeightHists


def doPUReweighting(hists2_2d_reweighted, puWeightHists):
    dataPUHist = puWeightHists['Data']
    for label in puWeightHists:
        puHist = puWeightHists[label]
        puHist.Scale(dataPUHist.Integral() / puHist.Integral())
        puWeightHists[label].Divide(dataPUHist, puHist)

        # Apply pu weights
        for layer, hist2d in hists2_2d_reweighted[label].iteritems():
            for xBin in range(1, hist2d.GetNbinsX() + 1):
                pu = hist2d.GetXaxis().GetBinCenter(xBin)
                puWeight = puWeightHists[label].GetBinContent(puWeightHists[label].FindBin(pu))

                for yBin in range(1, hist2d.GetNbinsY() + 1):
                    globalBin = hist2d.GetBin(xBin, yBin)
                    if (hist2d.GetBinContent(globalBin) > 0.0):
                        binContent = hist2d.GetBinContent(globalBin)
                        hist2d.SetBinContent(globalBin, binContent * puWeight)
    return hists2_2d_reweighted
