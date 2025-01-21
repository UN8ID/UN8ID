"""
UN8ID – A Heavy Globally Unique Identifier

THIS FILE IS A PROTOTYPE AND A DEMO IMPLEMENTATION
"""

import math
import time
from hashlib import sha256
from os import urandom

from UN8ID.utils import getmac


# #################################################################################################
# SYSTEM INTEGRITY CHECKS

# ... NOT IMPLEMENTED !


# #################################################################################################
# SECTION 1: TIME

# =================================================================================================
# CONSTANTS AND SYSTEM-VARIABLES

# The GRANULAR space
MAX_GRANULAR_BITS                      = 56
STATIC_PY_TIME_NS_RESOLUTION           = 9  # time.time_ns() always returns a number in the nanosecond range, regardless of the actual resolution
BITS_FOR_STATIC_PY_TIME_NS_RESOLUTION  = int(STATIC_PY_TIME_NS_RESOLUTION * math.log2(10) + 1)  # the largest binary length that a decimal value with x digits can represent
GRANULAR_LEFT_PADDING_SHIFT            = MAX_GRANULAR_BITS - BITS_FOR_STATIC_PY_TIME_NS_RESOLUTION

# system clock resolution as integer
_resolution_as_float = time.get_clock_info("time").resolution
CLOCK_RESOLUTION = 0
while not _resolution_as_float.is_integer():
    _resolution_as_float *= 10
    CLOCK_RESOLUTION += 1

# free bits in GRANULAR for the pseudo granular (counter)
N_COUNT_BITS = MAX_GRANULAR_BITS - int(CLOCK_RESOLUTION * math.log2(10) + 1)  # the largest binary length that a decimal value with x digits can represent


# =================================================================================================
# FACTORY


def TIME(buffer: bytearray, count_granular: int):
    _time_nanoseconds   = time.time_ns()
    seconds_since_epoch = _time_nanoseconds // 1_000_000_000  # nanoseconds to seconds

    time_granular   = _time_nanoseconds - seconds_since_epoch * 1_000_000_000  # extract partial seconds as integer

    granular_buffer = time_granular << GRANULAR_LEFT_PADDING_SHIFT  # left padding shift up to the bit length of GRANULAR

    granular_buffer = granular_buffer | count_granular  # insert pseudo granular

    buffer[0:5]   =  seconds_since_epoch .to_bytes(length=5, byteorder="big")
    buffer[5:12]  =  granular_buffer     .to_bytes(length=7, byteorder="big")


# =================================================================================================

# #################################################################################################
# SECTION 2: META

def META(buffer: bytearray, ver: int, S: bool):
    buffer[12] = 0  # RCV1
    buffer[13] = N_COUNT_BITS
    buffer[14] = 0  # RCV2
    buffer[15] = (U << 7) | (G << 6) | (S << 5) | ver


# #################################################################################################
# SECTION 3: PHYS

# =================================================================================================
# CONSTANTS AND SYSTEM-VARIABLES

# MAC-Address request
MAC_ID = getmac()
if MAC_ID is None:
    # no network card or MAC could not be retrieved
    MAC_ID = urandom(48)
    U = 0
    G = 0
else:
    # convert L/G and M/U bits
    _first_byte         = MAC_ID >> 40
    _node_multicast_bit = _first_byte & 0b00000001
    _node_local_bit     = _first_byte & 0b00000010
    U = not _node_multicast_bit
    G = not _node_local_bit


# =================================================================================================
# UTILS

# temp. buffer for the SHA-256 input
def FingerprintBuffer(ver: int) -> bytearray:
    fingerprint_buffer = bytearray(b'\0' * 16)
    fingerprint_buffer[0] = ver
    return fingerprint_buffer


# =================================================================================================
# FACTORY (VERSION 0)


def PHYSv0(buffer: bytearray, additional_seed: bytes):
    import threading

    try:
        # get current Thread-ID
        thread_id = threading.get_native_id()
        # Not supported by all systems.
        # Availability: Windows, FreeBSD, Linux, macOS, OpenBSD, NetBSD, AIX.
    except Exception:
        raise

    fingerprint_buffer = FingerprintBuffer(0)

    fingerprint_buffer[1:9]  = MAC_ID    .to_bytes(length=8, byteorder="big")
    fingerprint_buffer[9:17] = thread_id .to_bytes(length=8, byteorder="big")

    fingerprint_buffer.extend(additional_seed)

    buffer[16:48] = sha256(fingerprint_buffer).digest()


# =================================================================================================
# FACTORY (VERSION 1)

def PHYSv1(buffer: bytearray, private_key: int):

    fingerprint_buffer = FingerprintBuffer(1)

    fingerprint_buffer[1:9]  = MAC_ID      .to_bytes(length=8, byteorder="big")
    fingerprint_buffer[9:17] = private_key .to_bytes(length=8, byteorder="big")

    buffer[16:48] = sha256(fingerprint_buffer).digest()


# =================================================================================================


# #################################################################################################
# MAIN FACTORIES


# create the main buffer
def Buffer() -> bytearray:
    return bytearray(b'\0' * 48)


def UN8ID0(count_granular: int, additional_seed: bytes) -> bytearray:
    buffer = Buffer()

    TIME(
        buffer=buffer,
        count_granular=count_granular
    )
    META(
        buffer=buffer,
        ver=0,
        S=False
    )
    PHYSv0(
        buffer=buffer,
        additional_seed=additional_seed
    )

    return buffer


def UN8ID1(count_granular: int, private_key: int) -> bytearray:
    buffer = Buffer()

    TIME(
        buffer=buffer,
        count_granular=count_granular
    )
    META(
        buffer=buffer,
        ver=1,
        S=False
    )
    PHYSv1(
        buffer=buffer,
        private_key=private_key
    )

    return buffer


# #################################################################################################
# APPLICATION SAMPLE


class ApplicationSample:

    @staticmethod
    def _monotonic_count_granular():
        max_value = 2**N_COUNT_BITS
        while True:
            for c in range(max_value):
                yield c

    monotonic_count_granular = _monotonic_count_granular()

    private_key: int

    from pathlib import Path

    keyfile = Path(__file__).parent / "un8id.pk"

    if keyfile.exists():
        with open(keyfile, "rb") as f:
            private_key = int.from_bytes(f.read(), byteorder="big")
    else:
        from os import urandom

        _private_key = urandom(8)
        private_key = int.from_bytes(_private_key, byteorder="big")
        with open(keyfile, "wb") as f:
            f.write(_private_key)

    @staticmethod
    def _get_additional_seed():
        from os import urandom
        return urandom(1)

    @staticmethod
    def UN8ID0() -> bytearray:
        return UN8ID0(
            count_granular=next(ApplicationSample.monotonic_count_granular),
            additional_seed=ApplicationSample._get_additional_seed()
        )

    @staticmethod
    def UN8ID1() -> bytearray:
        return UN8ID1(
            count_granular=next(ApplicationSample.monotonic_count_granular),
            private_key=ApplicationSample.private_key
        )


# #################################################################################################
# DEMO


def demo_template(name, un8id, mask_fingerprint: bool = True):
    import base64
    import datetime

    sse = int.from_bytes(un8id[:5], "big")
    granular = int.from_bytes(un8id[5:12], "big")
    rcv1 = un8id[12]
    n_count_bits = un8id[13]
    rcv2 = un8id[14]
    ver = un8id[15]

    if mask_fingerprint:
        un8id[16:] = b'?' * 32

    fingerprint = bytes(un8id[16:])

    def readable_granular(val: int):
        val = str(val)
        return str(",").join(val[g:g + 3] for g in range(0, len(val), 3))

    print("===================", )
    print(name, )
    print("                 ", bytes(un8id))
    print("  ~hex            :", un8id.hex())
    print("  ~base64         :", base64.b64encode(un8id).decode())
    print("-------------------", )
    print("    .SSE          :", f"{sse:,}")
    print("      ~date       :", datetime.datetime.fromtimestamp(sse, tz=datetime.timezone.utc))
    print("    .GRANULAR     :", readable_granular(granular))
    print("      ~bits       :", bin(granular))
    print("      .real       :", readable_granular(granular >> n_count_bits))
    print("      .pseudo     :", granular & int("0b" + "1" * n_count_bits, 2))
    print("    .RCV1         :", rcv1)
    print("    .N_COUNT_BITS :", n_count_bits)
    print("    .RCV2         :", rcv2)
    print("    .VERSION      :", ver)
    print("      .U          :", ver & 0b10000000 and 1)
    print("      .G          :", ver & 0b01000000 and 1)
    print("      .S          :", ver & 0b00100000 and 1)
    print("      .VERSION    :", ver & 0b00011111)
    print("    .FINGERPRINT  :", fingerprint)
    print("      ~hex        :", fingerprint.hex())
    print("===================", )
    print("\n")


def demo_main():
    un8id = UN8ID0(0, b'')
    demo_template("UN8ID.0 (no count, no add. data)", un8id, False)

    un8id = UN8ID1(0, 0)
    demo_template("UN8ID.1 (no count, no key)", un8id)

    next(ApplicationSample.monotonic_count_granular)

    un8id = ApplicationSample.UN8ID0()
    demo_template("UN8ID.0 (count, add. data)", un8id, False)

    un8id = ApplicationSample.UN8ID1()
    demo_template("UN8ID.1 (count, key)", un8id, False)

    un8id = ApplicationSample.UN8ID1()
    demo_template("UN8ID.1 (count, key) (another)", un8id, False)


if __name__ == "__main__":
    demo_main()


# #################################################################################################

