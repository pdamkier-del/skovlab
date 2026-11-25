#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <random>
#include <vector>

int main(int argc, char** argv) {
    const std::filesystem::path out = argc>1 ? argv[1] : "results";
    std::filesystem::create_directories(out);
    std::ofstream csv(out/"kmp.csv");
    if (!csv) return 1;
    csv << "N,seed,left,right,Ti,Tj,cov,flux,balance,arrow\n" << std::setprecision(17);
    for (int n : {16,32,64}) for (int seed=1;seed<=48;seed++) {
        for (const auto temperatures : {std::array{1.,1.}, std::array{.25,1.75}, std::array{1.75,.25}}) {
            std::mt19937_64 rng(seed+11021*n);
            std::uniform_real_distribution<double> uniform(0,1);
            std::uniform_int_distribution<int> bond(0,n);
            std::exponential_distribution<double> exponential(1);
            const auto [left,right]=temperatures;
            std::vector<double> e(n);
            for (int i=0;i<n;i++) e[i]=(left+(right-left)*(i+1)/(n+1))*exponential(rng);
            double initial=0, supplied=0;
            for (double value:e) initial+=value;
            constexpr int samples=6000;
            const int stride=n, burn=40*n*n, i=n/4-1, j=3*n/4-1;
            double sx=0, sy=0, sxy=0, flux=0, arrow=0, px=0, py=0;
            for (int sweep=0;sweep<burn+samples*stride;sweep++) {
                for (int k=0;k<n+1;k++){
                    const int b=bond(rng);
                    const double f=uniform(rng);
                    if (b==0 || b==n) {
                        const int endpoint=b==0 ? 0 : n-1;
                        const double before=e[endpoint];
                        e[endpoint]=f*(before+(b==0?left:right)*exponential(rng));
                        supplied+=e[endpoint]-before;
                        if (sweep>=burn && b==0) flux+=e[endpoint]-before;
                    } else {
                        const double total=e[b-1]+e[b];
                        e[b-1]=f*total;
                        e[b]=(1-f)*total;
                    }
                }
                if (sweep>=burn && (sweep-burn)%stride==0){
                    const double x=e[i], y=e[j];
                    sx+=x;
                    sy+=y;
                    sxy+=x*y;
                    if (sweep>burn) arrow+=px*px*y-x*x*py;
                    px=x;
                    py=y;
                }
            }
            double final=0;
            for (double value:e) final+=value;
            csv<<n<<','<<seed<<','<<left<<','<<right<<','<<sx/samples<<','<<sy/samples<<','
               <<sxy/samples-(sx/samples)*(sy/samples)<<','<<flux/(samples*stride)<<','
               <<final-initial-supplied<<','<<arrow/(samples-1)<<'\n';
        }
    }
}
