from solax.inverter import Inverter, InverterError
from solax.inverters import (
    QVOLTHYBG33P,
    X1,
    X3,
    X3V34,
    X1Boost,
    X1HybridGen4,
    X1Mini,
    X1MiniV34,
    X1Smart,
    XHybrid,
)

# registry of inverters
REGISTRY = [
    XHybrid,
    X3,
    X3V34,
    X1,
    X1Mini,
    X1MiniV34,
    X1Smart,
    QVOLTHYBG33P,
    X1Boost,
    X1HybridGen4,
]


class DiscoveryError(Exception):
    """Raised when unable to discover inverter"""


async def discover(host, port, pwd="") -> Inverter:
    failures = []
    for inverter in REGISTRY:
        for i in inverter.build_all_variants(host, port, pwd):
            try:
                await i.get_data()
                return i
            except InverterError as ex:
                failures.append(ex)
    msg = (
        "Unable to connect to the inverter at "
        f"host={host} port={port}, or your inverter is not supported yet.\n"
        "Please see https://github.com/squishykid/solax/wiki/DiscoveryError\n"
        f"Failures={str(failures)}"
    )
    raise DiscoveryError(msg)
