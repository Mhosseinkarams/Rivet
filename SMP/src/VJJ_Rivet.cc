// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/DressedLeptons.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Projections/PromptFinalState.hh"
#include "Rivet/Projections/LeadingParticlesFinalState.hh"


namespace Rivet {


  /// @brief Add a short analysis description here
  class VJJ_Rivet : public Analysis {
  public:

   VJJ_Rivet()
      : Analysis("VJJ_Rivet")
       {        }
    
    //@}
    
    
    public:




    /// @name Analysis methods
    ///@{

    /// Book histograms and initialise projections before the run
    void init() {

      const FinalState fs(Cuts::abseta < 4.9);
      FastJets conefinder(fs, FastJets::D0ILCONE, 0.4);
      declare(conefinder, "ConeFinder");

      // FinalState of prompt photons and bare muons and electrons in the event
      LeadingParticlesFinalState photonfs(FinalState(Cuts::abseta < 1.4442 && Cuts::pT > 200*GeV));
      photonfs.addParticleId(PID::PHOTON);
      declare(photonfs, "LeadingPhoton");


      // Book histograms
      // specify custom binning
      book(_hphoton_pt, 1,1,1);
      //book(_hphoton_eta,"photon_eta",20,-10,10);
      book(_hmjj, 3,1,1);
      //book(_hjj_delta_eta,"jj_delta_eta", 20,-10,10);
      book(_hjj_delta_phi, 2,1,1);     
      //book(_hleading_jet_pt,"leading_jet_pt", 20,0,10000);
      //book(_hsubleading_jet_pt,"subleading_jet_pt", 20,0,10000);
      //book(_hleading_jet_eta,"leading_jet_eta", 20,-10,10);
      //      book(_hsubleading_jet_eta,"subleading_jet_eta", 20,-10,10);
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      //      cout<<"start"<<endl;
      Particles photons = apply<LeadingParticlesFinalState>(event, "LeadingPhoton").particles();
      if (photons.size() < 1) vetoEvent;
      const Particle& leadingPhoton = photons[0];
      //cout<<"photon_pt"<<leadingPhoton.pt()<<endl;
      const Jets& jets = apply<FastJets>(event, "ConeFinder").jetsByPt(50.0*GeV);
      if (jets.size() < 2) vetoEvent;
      //cout<<"number of jets"<<jets.size()<<endl;
      // Apply additional cuts on photon and jets
      if (leadingPhoton.pt() < 200*GeV || std::abs(leadingPhoton.eta()) > 1.4442) vetoEvent;
      // cout<<"selected photon pt"<<leadingPhoton.pt()<<endl;
      if (jets[0].pt() < 50*GeV || std::abs(jets[0].eta()) > 4.7 ||
      jets[1].pt() < 50*GeV || std::abs(jets[1].eta()) > 4.7) vetoEvent;

      // Check delta R between photon and jets
      if (deltaR(leadingPhoton, jets[0]) < 0.4 || deltaR(leadingPhoton, jets[1]) < 0.4) vetoEvent;

      // Calculate invariant mass of dijet system
      FourMomentum j0(jets[0].momentum());
      FourMomentum j1(jets[1].momentum());
      double mjj = FourMomentum(j0 + j1).mass();
      //cout<<"mjj"<<mjj<<endl;

      // Apply additional cuts on mjj and delta eta jj
      if (mjj < 500 || std::abs(jets[0].eta() - jets[1].eta()) < 2.5) vetoEvent;
      //cout<<"selected jets mjj"<<mjj<<endl;
      // Fill histograms
      _hphoton_pt->fill(leadingPhoton.pt());
      //_hphoton_eta->fill(leadingPhoton.eta());
      _hmjj->fill(mjj);
      //_hjj_delta_eta->fill(std::abs(jets[0].eta() - jets[1].eta()));
      _hjj_delta_phi->fill(jets[0].phi()-jets[1].phi());
      //_hleading_jet_pt->fill(jets[0].pt());
      //_hsubleading_jet_pt->fill(jets[1].pt());
      //_hleading_jet_eta->fill(jets[0].eta());
      //_hsubleading_jet_eta->fill(jets[1].eta());

    }


    /// Normalise histograms etc., after the run
    void finalize() {

      scale(_hphoton_pt, 25.75 * (crossSection() / picobarn) / sumW());
      //scale(_hphoton_eta, 25.75 * (crossSection() / picobarn) / sumW());
      scale(_hmjj, 25.75 * (crossSection() / picobarn) / sumW());
      //scale(_hjj_delta_eta, 25.75 * (crossSection() / picobarn) / sumW());
      scale(_hjj_delta_phi, 25.75 * (crossSection() / picobarn) / sumW());
      //scale(_hleading_jet_pt, 25.75 * (crossSection() / picobarn) / sumW());
      //scale(_hsubleading_jet_pt, 25.75 * (crossSection() / picobarn) / sumW());
      //scale(_hleading_jet_eta, 25.75 * (crossSection() / picobarn) / sumW());
      //scale(_hsubleading_jet_eta, 25.75 * (crossSection() / picobarn) / sumW());

      
    }

    ///@}

  private :
    /// @name Histograms
    ///@{
    Histo1DPtr _hphoton_pt;
    Histo1DPtr _hphoton_eta;
    Histo1DPtr _hmjj;
    Histo1DPtr _hjj_delta_eta;
    Histo1DPtr _hjj_delta_phi;
    Histo1DPtr _hleading_jet_pt;
    Histo1DPtr _hsubleading_jet_pt;
    Histo1DPtr _hleading_jet_eta;
    Histo1DPtr _hsubleading_jet_eta;


    ///@}

  };


    DECLARE_RIVET_PLUGIN(VJJ_Rivet);



}