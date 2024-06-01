import ROOT
from array import array


ranges = {
    'bin1': {'high': 250, 'low': 200},
    'bin2': {'high': 350, 'low': 250},
    'bin3': {'high': 700, 'low': 350},
}  
root_file_path = "Diff_vjj/mjj.root"
file = ROOT.TFile(root_file_path,"READ")
bins = ['bin1','bin2','bin3']
years = ['2016','2016pre', '2016post','2017', '2018']
total_sig_histograms_by_bin = {}
total_sig_histograms_by_year_bin = {}


total_sig_histograms_by_bin = {}
total_sig_histograms_by_year_bin = {}

for b in bins:
    print(b)
    total_sig_histograms_by_bin[b] = ROOT.TH1D(f"TotalSig_{b}", "TotalSig", 7, 0, 1)
    for i in range(len(file.GetListOfKeys())):

        Folder = file.GetListOfKeys()[i].ReadObj()
        for y in years:
            if f'SR_{y}_SR_{b}_{y}_prefit' in Folder.GetName():
                print(y)
                obj = Folder.Get('TotalSig')
                total_sig_histograms_by_year_bin[y] = {b: obj.Clone()}
                total_sig_histograms_by_bin[b].Add(obj)  # Add the histogram to the corresponding bin
                print(f"Integral of TotalSig histograms for {b} in year {y} : {obj.Integral()}")
                print(total_sig_histograms_by_bin[b].Integral())
    print(b)
    print(total_sig_histograms_by_bin)
    integral = total_sig_histograms_by_bin[b].Integral()
    print(f"Integral of TotalSig histograms for {b} : {integral}")
    
New_histograms_by_bin = {}
for b in bins:
    integral = total_sig_histograms_by_bin[b].Integral()
    print(f"Integral of TotalSig histograms for {b} : {integral}")
    New_histograms_by_bin[b] =  ROOT.TH1D(b, b, 1, ranges[b]['low'], ranges[b]['high'])
    # Set the content of the bin to the integral value
    New_histograms_by_bin[b].SetBinContent(1, integral)    
# Create a canvas to draw histograms
canvas = ROOT.TCanvas("canvas", "Histograms", 800, 600)

# Define the bin edges
bin_edges = [200, 250, 350, 700]

# Create the histogram with fixed binning
full_hist = ROOT.TH1D("full", "Full", len(bin_edges) - 1, array('d', bin_edges))

# Create a legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)

# Create histograms for each bin and add them to the stack
for b in bins:
    integral = total_sig_histograms_by_bin[b].Integral()
    print(f"Integral of TotalSig histograms for {b} : {integral}")
    hist = ROOT.TH1D(b, b, 1, ranges[b]['low'], ranges[b]['high'])
    # Set the content of the bin to the integral value
    hist.SetBinContent(1, integral)
    full_hist.Add(hist)
    legend.AddEntry(hist, b)

# Draw the stacked histogram
canvas.cd()
full_hist.Draw()
# stack.GetXaxis().SetTitle("X Axis Title")
# stack.GetYaxis().SetTitle("Y Axis Title")
legend.Draw()
# canvas.Update()
canvas.SaveAs("test.pdf")