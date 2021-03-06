#ifndef SCSI_STATE_VECTOR_H
#define SCSI_STATE_VECTOR_H

#include <ostream>

#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/storage.hpp>

#include "../base.h"

/** @brief Simulation state which include only a vector
 */
struct VectorState : public StateBase
{
    enum {maxsize=7};
    enum param_t {
        PS_X, PS_PX, PS_Y, PS_PY, PS_S, PS_PS
    };

    VectorState(const Config& c);
    virtual ~VectorState();

    virtual void assign(const StateBase& other);

    typedef boost::numeric::ublas::vector<double,
                    boost::numeric::ublas::bounded_array<double, maxsize>
    > value_t;

    virtual void show(std::ostream& strm) const;

    value_t state;

    virtual bool getArray(unsigned idx, ArrayInfo& Info);

    virtual VectorState* clone() const {
        return new VectorState(*this, clone_tag());
    }

protected:
    VectorState(const VectorState& o, clone_tag);
};

#endif // SCSI_STATE_VECTOR_H
