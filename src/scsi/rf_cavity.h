#ifndef RF_CAVITY_H
#define RF_CAVITY_H

#endif // RF_CAVITY_H

#include <boost/numeric/ublas/matrix.hpp>


// Phase space dimension; including vector for orbit/1st moment.
# define PS_Dim Moment2State::maxsize // Set to 7; to include orbit.


class CavDataType {
// Cavity on-axis longitudinal electric field vs. s.
public:
    std::vector<double> s,     // s coordinate [m]
                        Elong; // Longitudinal Electric field [V/m].

    void RdData(std::fstream &inf);
    void show(std::ostream&, const int) const;
    void show(std::ostream&) const;
};


class CavTLMLineType {
public:
    std::vector<double> s;         // Longitudinal position [m].
    std::vector<std::string> Elem;
    std::vector<double> E0,
                        T,
                        S,
                        Accel;

    void clear(void);
    void set(const double, const std::string &, const double,
             const double, const double, const double);
    void show(std::ostream& strm, const int) const;
    void show(std::ostream& strm) const;
};


void TransitFacMultipole(const int cavi, const std::string &flabel, const double IonK,
                         double &T, double &S);

void TransFacts(const int cavilabel, double beta, const int gaplabel, const double EfieldScl,
                double &Ecen, double &T, double &Tp, double &S, double &Sp, double &V0);

void EvalGapModel(const double dis, const double IonW0, Particle &real, const double IonFy0,
                  const double k, const double Lambda, const double Ecen,
                  const double T, const double S, const double Tp, const double Sp, const double V0,
                  double &IonW_f, double &IonFy_f);

double GetCavPhase(const int cavi, Particle ref, const double IonFys, const double multip);

struct ElementRFCavity : public Moment2ElementBase
{
    // Transport matrix for an RF Cavity.
    typedef Moment2ElementBase       base_t;
    typedef typename base_t::state_t state_t;

    CavDataType    CavData;
    std::fstream   inf1, inf2, inf3;
    CavTLMLineType CavTLMLineTab;

    ElementRFCavity(const Config& c)
        :base_t(c)
    {
        std::string cav_type = c.get<std::string>("cavtype");
        double L             = c.get<double>("L")*MtoMM;         // Convert from [m] to [mm].

        std::string CavType      = conf().get<std::string>("cavtype");
        std::string Eng_Data_Dir = conf().get<std::string>("Eng_Data_Dir", "");

        if (CavType == "0.041QWR") {
            inf1.open((Eng_Data_Dir+"/Multipole41/thinlenlon_41.txt").c_str(), std::ifstream::in);
            if (!inf1.is_open()) {
                std::cout << "ElementRFCavity: could not open thinlenlon_41.txt\n";
                exit(1);
            }
            inf2.open((Eng_Data_Dir+"/axisData_41.txt").c_str(), std::ifstream::in);
            if (!inf2.is_open()) {
                std::cout << "ElementRFCavity: could not open axisData_41.txt\n";
                exit(1);
            }
            CavData.RdData(inf2);
            inf3.open((Eng_Data_Dir+"/Multipole41/CaviMlp_41.txt").c_str(), std::ifstream::in);
            if (!inf3.is_open()) {
                std::cout << "ElementRFCavity: could not open CaviMlp_41.txt\n";
                exit(1);
            }
        } else if (conf().get<std::string>("cavtype") == "0.085QWR") {
            inf1.open((Eng_Data_Dir+"/Multipole85/thinlenlon_85.txt").c_str(), std::ifstream::in);
            if (!inf1.is_open()) {
                std::cout << "ElementRFCavity: could not open thinlenlon_85.txt\n";
                exit(1);
            }
            inf2.open((Eng_Data_Dir+"/axisData_85.txt").c_str(), std::ifstream::in);
            if (!inf2.is_open()) {
                std::cout << "ElementRFCavity: could not open axisData_85.txt\n";
                exit(1);
            }
            CavData.RdData(inf2);
            inf3.open((Eng_Data_Dir+"/Multipole85/CaviMlp_85.txt").c_str(), std::ifstream::in);
            if (!inf3.is_open()) {
                std::cout << "ElementRFCavity: could not open CaviMlp_85.txt\n";
                exit(1);
            }
        } else if (conf().get<std::string>("cavtype") == "0.29HWR") {
            inf1.open((Eng_Data_Dir+"/Multipole29/thinlenlon_29.txt").c_str(), std::ifstream::in);
            if (!inf1.is_open()) {
                std::cout << "ElementRFCavity: could not open thinlenlon_29.txt\n";
                exit(1);
            }
            inf2.open((Eng_Data_Dir+"/axisData_29.txt").c_str(), std::ifstream::in);
            if (!inf2.is_open()) {
                std::cout << "ElementRFCavity: could not open axisData_29.txt\n";
                exit(1);
            }
            CavData.RdData(inf2);
            inf3.open((Eng_Data_Dir+"/Multipole29/CaviMlp_29.txt").c_str(), std::ifstream::in);
            if (!inf3.is_open()) {
                std::cout << "ElementRFCavity: could not open CaviMlp_29.txt\n";
                exit(1);
            }
        } else if (conf().get<std::string>("cavtype") == "0.53HWR") {
            inf1.open((Eng_Data_Dir+"/Multipole53/thinlenlon_53.txt").c_str(), std::ifstream::in);
            if (!inf1.is_open()) {
                std::cout << "ElementRFCavity: could not open thinlenlon_53.txt\n";
                exit(1);
            }
            inf2.open((Eng_Data_Dir+"/axisData_53.txt").c_str(), std::ifstream::in);
            if (!inf2.is_open()) {
                std::cout << "ElementRFCavity: could not open axisData_53.txt\n";
                exit(1);
            }
            CavData.RdData(inf2);
            inf3.open((Eng_Data_Dir+"/Multipole53/CaviMlp_53.txt").c_str(), std::ifstream::in);
            if (!inf3.is_open()) {
                std::cout << "ElementRFCavity: could not open CaviMlp_53.txt\n";
                exit(1);
            }
        } else {
            std::ostringstream strm;
            strm << "*** InitRFCav: undef. cavity type: " << CavType << "\n";
            throw std::runtime_error(strm.str());
        }

        transfer_raw(state_t::PS_X, state_t::PS_PX) = L;
        transfer_raw(state_t::PS_Y, state_t::PS_PY) = L;
        // For total path length.
//        transfer(state_t::PS_S, state_t::PS_S)  = L;
    }

    void GetCavMatParams(const int cavi,
                         const double beta_tab[], const double gamma_tab[], const double IonK[]);

    void GetCavMat(const int cavi, const int cavilabel, const double Rm, Particle &real,
                   const double EfieldScl, const double IonFyi_s,
                   const double IonEk_s, const double fRF, value_mat &M);

    void GenCavMat(const int cavi, const double dis, const double EfieldScl, const double TTF_tab[],
                   const double beta_tab[], const double gamma_tab[], const double Lambda,
                   Particle &real, const double IonFys[], const double Rm, value_mat &M);

    void PropagateLongRFCav(Particle &ref);

    void InitRFCav(Particle &real, double &accIonW,
                   double &avebeta, double &avegamma, value_mat &M);

    void GetCavBoost(const CavDataType &CavData, Particle &state, const double IonFy0, const double fRF,
                     const double EfieldScl, double &IonFy, double &accIonW);

    void TransFacts(const int cavilabel, double beta, const double CaviIonK, const int gaplabel, const double EfieldScl,
                    double &Ecen, double &T, double &Tp, double &S, double &Sp, double &V0);

    void TransitFacMultipole(const int cavi, const std::string &flabel, const double CaviIonK,
                             double &T, double &S);

    virtual ~ElementRFCavity() {}

    virtual void advance(StateBase& s)
    {
        state_t&  ST = static_cast<state_t&>(s);
        using namespace boost::numeric::ublas;

        // IonEk is Es + E_state; the latter is set by user.

        if ((int)ST.clng){
            // limited longitudinal run
            ST.ref.recalc();
            ElementRFCavity::PropagateLongRFCav(ST.ref);
            ST.pos += length;
            ST.ref.recalc();

        } else {

            ST.real.recalc();
            //@-
            ST.ref.recalc();

            // mod for python interface by KF
            if(ST.real.IonEk!=last_Kenergy_in || ST.real.IonZ==ST.ref.IonZ) {
                // need to re-calculate energy dependent terms

                recompute_matrix(ST); // updates transfer and last_Kenergy_out

                get_misalign(ST);

                ST.real.recalc();
                //@-
                ST.ref.recalc();

            }

            // recompute_matrix only called when ST.IonEk != last_Kenergy_in.
            // Matrix elements are scaled with particle energy.

            ST.pos += length;

            ST.moment0 = prod(misalign, ST.moment0);
            ST.moment0 = prod(transfer, ST.moment0);

            ST.moment0[state_t::PS_S]  = ST.real.phis - ST.ref.phis;
            ST.moment0[state_t::PS_PS] = (ST.real.IonEk-ST.ref.IonEk)/MeVtoeV;

            ST.moment0 = prod(misalign_inv, ST.moment0);

            scratch  = prod(misalign, ST.state);
            ST.state = prod(scratch, trans(misalign));

            scratch  = prod(transfer, ST.state);
            ST.state = prod(scratch, trans(transfer));

            scratch  = prod(misalign_inv, ST.state);
            ST.state = prod(scratch, trans(misalign_inv));

            }
    }

    virtual void recompute_matrix(state_t& ST)
    {
        // Re-initialize transport matrix.
        transfer = boost::numeric::ublas::identity_matrix<double>(state_t::maxsize);

        last_Kenergy_in = ST.real.IonEk;

        // J.B. Bug in TLM.
        double SampleIonK = ST.real.SampleIonK;

        ElementRFCavity::PropagateLongRFCav(ST.ref);

        last_Kenergy_out = ST.real.IonEk;

        // Define initial conditions.
        double accIonW, avebeta, avegamma;

        ElementRFCavity::InitRFCav(ST.real, accIonW, avebeta, avegamma, transfer);

        // J.B. Bug in TLM.
        ST.real.SampleIonK = SampleIonK;
   }

    virtual const char* type_name() const {return "rfcavity";}
};

