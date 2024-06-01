#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/PromptFinalState.hh"

namespace Rivet {

  class CMS_2024_PAS_SMP_24_005 : public Analysis {
  public:

    CMS_2024_PAS_SMP_24_005()
      : Analysis("CMS_2024_PAS_SMP_24_005")
    { }

    void init() {
      // Initialize projections
      const FinalState fs(Cuts::abseta < 4.7);
      declare(fs, "FS");

      FastJets antikt4Jets(fs, FastJets::ANTIKT, 0.4);
      declare(antikt4Jets, "AntiKt4Jets");

      PromptFinalState promptPhotons(Cuts::abseta < 1.4442 && Cuts::pT > 200*GeV && Cuts::abspid == PID::PHOTON);
      declare(promptPhotons, "PromptPhotons");

      // Book histograms
      book(_h_photon_pt, "Photon_pT", 50, 0, 700);
      book(_h_mjj, "Mjj", 50, 0, 2000);
      book(_h_jj_delta_phi, "DeltaPhi_jj", 50, -M_PI, M_PI);
    }

    void analyze(const Event& event) {
      const Particles& photons = apply<PromptFinalState>(event, "PromptPhotons").particles();

      if (photons.size() < 1) vetoEvent;

      const Jets& jets = apply<FastJets>(event, "AntiKt4Jets").jetsByPt(50*GeV);

      if (jets.size() < 2) vetoEvent;

      const Particle& leadingPhoton = photons[0];
      if (leadingPhoton.pt() <= 200*GeV || fabs(leadingPhoton.eta()) >= 1.4442) vetoEvent;

      const Jet& jet1 = jets[0];
      const Jet& jet2 = jets[1];
      if (jet1.pt() <= 50*GeV || fabs(jet1.eta()) >= 4.7 ||
          jet2.pt() <= 50*GeV || fabs(jet2.eta()) >= 4.7) vetoEvent;

      if (deltaR(leadingPhoton, jet1) <= 0.4 || deltaR(leadingPhoton, jet2) <= 0.4) vetoEvent;

      FourMomentum j0 = jet1.momentum();
      FourMomentum j1 = jet2.momentum();
      double mjj = (j0 + j1).mass();
      if (mjj <= 500) vetoEvent;

      double deltaEta_jj = fabs(jet1.eta() - jet2.eta());
      if (deltaEta_jj < 2.5) vetoEvent;
      
      // Fill histograms
      double weight = event.weight();
      _h_photon_pt->fill(leadingPhoton.pt(),weight);
      _h_mjj->fill(mjj,weight);
      _h_jj_delta_phi->fill(deltaPhi(jet1, jet2),weight);
    }

    void finalize() {
      // Normalize histograms to cross-section
      const double norm = crossSection() / sumW();
      scale(_h_photon_pt, norm);
      scale(_h_mjj, norm);
      scale(_h_jj_delta_phi, norm);
    }

  private:
    Histo1DPtr _h_photon_pt;
    Histo1DPtr _h_mjj;
    Histo1DPtr _h_jj_delta_phi;
  };

  DECLARE_RIVET_PLUGIN(CMS_2024_PAS_SMP_24_005);

}
