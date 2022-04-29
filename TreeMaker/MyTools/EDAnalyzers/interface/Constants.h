# ifndef Constants_H
# define Constants_H


# include <iostream>
# include <map>
# include <stdlib.h>
# include <string>
# include <type_traits>
# include <utility>
# include <vector>

# include <TH1F.h>
# include <TH2F.h>
# include <TMatrixD.h>
# include <TTree.h> 
# include <TVectorD.h> 


namespace Constants
{
    //const double LARGEVAL_POS = std::numeric_limits<double>::max();
    const double LARGEVAL_POS = +99999;
    const double LARGEVAL_NEG = -99999;
    
    const double DEFAULT_BRANCH_ENTRY = -99;
    
    const double CONSTI_EL_DR_MAX = 0.01;
    const double CONSTI_MU_DR_MAX = 0.01;
}


# endif
