#include "sai_vs.h"
#include "sai_vs_internal.h"

VS_GENERIC_QUAD(SAMPLEPACKET,samplepacket);

const sai_samplepacket_api_t vs_samplepacket_api = {

    VS_GENERIC_QUAD_API(samplepacket)
};
