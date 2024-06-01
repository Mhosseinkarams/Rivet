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
  class CMS_1601_PAS_SMP_19_005 : public Analysis {
  public:

    CMS_1601_PAS_SMP_19_005()
      : Analysis("CMS_1601_PAS_SMP_19_005")
    {     std::cout<<"I am in constructor"<<std::endl;   }

    //@}
  public:

    /// @name Analysis methods
    /// Book histograms and initialise projections before the run
    void init() {
      std::cout<<"In init method of CMS_2024_PAS_SMP_24_005.cc"<<std::endl;
      const FinalState fs(Cuts::abseta < 4.9);
      FastJets conefinder(fs, FastJets::D0ILCONE, 0.4);
      declare(conefinder, "ConeFinder");
      std::cout<<"Jetfinder done"<<std::endl;

      // FinalState of prompt photons and bare muons and electrons in the event
      LeadingParticlesFinalState photonfs(FinalState(Cuts::abseta < 1.4442 && Cuts::pT > 200*GeV));
      photonfs.addParticleId(PID::PHOTON);
      declare(photonfs, "LeadingPhoton");


      // Book histograms
      cout<<"booking photon pt"<<endl;
      book(_h_photon_pt,1,1,1);
      _h_photon_pt->Sumw2();
     // cout<<"booking mjj"<<endl;
      //book(_h_mjj,3,1,1);
      //cout<<"booking delta phi"<<endl;
      //book(_h_jj_delta_phi,2,1,1);

    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {

      Particles photons = apply<LeadingParticlesFinalState>(event, "LeadingPhoton").particles();
      if (photons.size() < 1) vetoEvent;
      const Particle& leadingPhoton = photons[0];
      const Jets& jets = apply<FastJets>(event, "ConeFinder").jetsByPt(50.0*GeV);
      if (jets.size() < 2) vetoEvent;

      if (leadingPhoton.pt() < 200*GeV) vetoEvent;
      if (std::abs(leadingPhoton.eta()) > 1.442) vetoEvent;

      if (jets[0].pt() < 50*GeV) vetoEvent;
      if (std::abs(jets[0].eta()) > 4.7) vetoEvent;
      if (jets[1].pt() < 50*GeV ) vetoEvent;
      if (std::abs(jets[1].eta()) > 4.7) vetoEvent;


      if (deltaR(leadingPhoton, jets[0]) < 0.4) vetoEvent;
      if (deltaR(leadingPhoton, jets[1]) < 0.4) vetoEvent;


      FourMomentum j0(jets[0].momentum());
      FourMomentum j1(jets[1].momentum());
      double mjj = FourMomentum(j0 + j1).mass();





      if (mjj < 500 ) vetoEvent;
      if (std::abs(jets[0].eta() - jets[1].eta()) < 1.5) vetoEvent;
      cout<<"mjj = "<<mjj<<"pt = "<<leadingPhoton.pt()<<"delta phi = "<<jets[0].phi()-jets[1].phi()<<endl;

      // Fill histograms
      //double weight = event.weight();
     // cout<<"weight = "<<weight<<endl;
      _h_photon_pt->fill(leadingPhoton.pt());
      //_h_mjj->fill(mjj);
      //_h_jj_delta_phi->fill(deltaPhi(jets[0], jets[1]));
    }

    void finalize() {
      // Normalize histograms to cross-section
      //const double norm = crossSection() * 6.791/picobarn/sumOfWeights();
      const double norm = crossSection()/sumOfWeights();
      scale(_h_photon_pt, norm);
      //scale(_h_mjj, norm);
      //scale(_h_jj_delta_phi, norm);
    }

  private:
    Histo1DPtr _h_photon_pt;
    Histo1DPtr _h_mjj;
    Histo1DPtr _h_jj_delta_phi;
  };

  DECLARE_RIVET_PLUGIN(CMS_1601_PAS_SMP_19_005);

}
