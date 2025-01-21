<div>Date: Jan. 20, 2025</div>
<div>Author: Adrian F. Hoefflin [srccircumflex] (srccircumflex-un8id@outlook.com)</div>

[![logo](https://raw.githubusercontent.com/UN8ID/UN8ID/master/logo.png)](https://github.com/UN8ID/UN8ID)

# UN8ID – A Heavy Globally Unique Identifier

## Licence and Copyright Notice

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
<a property="dct:title" rel="cc:attributionURL" href="https://github.com/UN8ID">
UN8ID
</a>
© 2025 by
<a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/UN8ID">
Adrian F. Höfflin [srccircumflex]
</a>
is licensed under
<a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Creative Commons Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""></a></p> 

<details>

<summary>

## Table of Contents

</summary>

* [Abstract](#abstract)
* [Background](#background)
* [Design](#design)
  + [Property: Uniqueness that can be sorted in time:](#property-uniqueness-that-can-be-sorted-in-time)
  + [Property: Physically anonymous uniqueness:](#property-physically-anonymous-uniqueness)
  + [Advantages over conventional UIDs](#advantages-over-conventional-uids)
* [Specification](#specification)
  + [Versions](#versions)
    - [UN8ID.0](#un8id0)
    - [UN8ID.1](#un8id1)
  + [Binary Layout and Byte Order](#binary-layout-and-byte-order)
  + [Section 1: TIME (bit 0-95/octet 0-11) (96 bits/12 bytes)](#section-1-time-bit-0-95octet-0-11-96-bits12-bytes)
    - [Section 1. Component 1: SSE (bit 0-39/octet 0-4) (40 bits/5 bytes)](#section-1-component-1-sse-bit-0-39octet-0-4-40-bits5-bytes)
    - [Section 1. Component 2: GRANULAR (bit 40-95/octet 5-11) (56 bits/7 bytes)](#section-1-component-2-granular-bit-40-95octet-5-11-56-bits7-bytes)
  + [Section 2: META (bit 96-127/octet 12-15) (32 bits/4 bytes)](#section-2-meta-bit-96-127octet-12-15-32-bits4-bytes)
    - [Section 2 Component 1: RCV1 (Bit 96-103/Octet 12) (8 Bits/1 Bytes)](#section-2-component-1-rcv1-bit-96-103octet-12-8-bits1-bytes)
    - [Section 2. Component 2: N_COUNT_BITS (bit 104-111/octet 13) (8 bits/1 bytes)](#section-2-component-2-n_count_bits-bit-104-111octet-13-8-bits1-bytes)
    - [Section 2. Component 3: RCV2 (bit 112-119/octet 14) (8 bits/1 bytes)](#section-2-component-3-rcv2-bit-112-119octet-14-8-bits1-bytes)
    - [Section 2. Component 3: U|G|S| VERSION (Bit 120-127/Octet 15) (8 Bits/1 Bytes)](#section-2-component-3-ugs-version-bit-120-127octet-15-8-bits1-bytes)
  + [Section 3. Component: FINGERPRINT (Bit 128-383/Octet 16-47) (256 Bits/32 Bytes)](#section-3-component-fingerprint-bit-128-383octet-16-47-256-bits32-bytes)
    - [VERSION 0](#version-0)
      * [Layout for Inputs](#layout-for-inputs)
      * [VER (Bit 0-7/Octet 0) (8 bits/1 byte)](#ver-bit-0-7octet-0-8-bits1-byte)
      * [MAC (Bit 8-71/Octet 1-8) (64 bits/8 bytes)](#mac-bit-8-71octet-1-8-64-bits8-bytes)
      * [TID (Bit 72-135/Octet 9-16) (64 bits/8 bytes)](#tid-bit-72-135octet-9-16-64-bits8-bytes)
      * [RND (Bit 136-159/octet 17-19) (24 bits/3 bytes)](#rnd-bit-136-159octet-17-19-24-bits3-bytes)
    - [VERSION 1](#version-1)
      * [Layout for Inputs](#layout-for-inputs-1)
      * [VER (Bit 0-7/Octet 0) (8 bits/1 byte)](#ver-bit-0-7octet-0-8-bits1-byte-1)
      * [MAC (Bit 8-71/octet 1-8) (64 bits/8 bytes)](#mac-bit-8-71octet-1-8-64-bits8-bytes)
      * [KEY (Bit 72-135/octet 9-16) (64 bits/8 bytes)](#key-bit-72-135octet-9-16-64-bits8-bytes)
  + [Coding](#coding)
* [Basic Algorithm](#basic-algorithm)
  + [System check](#system-check)
  + [Section 1: TIME](#section-1-time)
  + [Section 2: META](#section-2-meta)
  + [Section 3: FINGERPRINT](#section-3-fingerprint)
* [Security Considerations](#security-considerations)
  + [Correlation between secure obfuscation of the MAC-Address and collision probability in FINGERPRINT](#correlation-between-secure-obfuscation-of-the-mac-address-and-collision-probability-in-fingerprint)
  + [Duration d of a brute force attack against the FINGERPRINT to find the MAC-Address](#duration-d-of-a-brute-force-attack-against-the-fingerprint-to-find-the-mac-address)
    - [@VERSION 0:](#version-0-1)
    - [@VERSION 1:](#version-1-1)
  + [Collision probabilities](#collision-probabilities)
    - [@VERSION 0:](#version-0-2)
    - [@VERSION 1:](#version-1-2)
* [Appendix A: Prototype Implementation](#appendix-a-prototype-implementation)
* [Appendix B: Application Sample](#appendix-b-application-sample)
* [Appendix C: Demo](#appendix-c-demo)
* [Appendix D: Sample Demo Output](#appendix-d-sample-demo-output)

</details>

## Abstract

UN8ID is a 384-bit (48-byte) sequence that can be used for truly unique identification in space and time. 
A central registry is not necessary in the direct sense.

In contrast to conventional unique identifiers (UIDs), a UN8ID is significantly more complex to create 
and requires a larger memory space.

UN8IDs should therefore be used, if at all, as a supplement to common UIDs or in extreme use cases.

## Background

UN8ID began as a mind game for a unique identification guaranteed on a
global level in space and time.

The uniqueness should be achieved under the following conditions:
1. not just theoretically by including random values (e.g. UUIDv4, UUIDv6, UUIDv7, UUIDv8, ULID) [^1] [^2]
2. not through the direct use of the MAC-Address (e.g. UUID1, UUIDv6, UUIDv8) [^1]

In addition, a UN8ID should contain a timestamp for chronological assignment and sorting that also 
works without coding for a UN8ID by itself. For greater compatibility, the timestamp should 
be designed for different precessions.

## Design

The core characteristic of a UN8ID is a real uniqueness in time and space with simultaneous 
anonymity of the physical identification.

### Property: Uniqueness that can be sorted in time:

The first section of a UN8ID consists of a 96 bit (12 bytes) long timestamp which is divided into a 
40 bit (5 bytes) long component for whole seconds since the epoch and a 56 bit (7 bytes) long component 
for a granulation. 
The largest timestamp that can be represented corresponds to the year 36,812 A.D.

The granulation can be defined based on the precision of the system clock or/with a 
pseudo-granulation using a manual counter.

The high value of granulation ensures that a powerful system does not generate the same timestamp 
several times. For example, even after including a nanosecond, there is still room left for 67,108,863 
additional subdivisions. 
Generally there should be no collisions at the present time, even with high-performance chips.
For a rough evaluation, the number of instructions that a system can perform per time unit could be estimated: 
For example, an *AMD Ryzen Threadripper 3990X (64 core) (2020)* can execute 
around 2,300 instructions per nanosecond [^3]. 
The number of operations that a UN8ID setting itself requires varies greatly depending on the implementation 
and hardware.

The scope of the pseudo-granulation of a UN8ID is stored within the second section. 
This allows the significance of a time stamp to be determined. The specification does not define the pseudo part; 
a monotonic counter can also be used, which is not reset for each time unit.

### Property: Physically anonymous uniqueness:

The third section of a UN8ID consists of a 256 bit (32 byte) long hash value. 
The algorithm to be used is SHA-256 (RFC6234[^4]).

The input consists of at least 136 bits (17 bytes) made up of the UN8ID version and 64 bits (8 bytes) 
each of the IEEE 802 MAC-Address[^5] as a 48-bit integer and the current native Thread-ID. In addition, 
a sequence of undefined content can be appended to the input, which may also change for each generation.

By entering the MAC-Address, a globally unique physical identifier is guaranteed. 
Entering the native Thread-ID ensures local uniqueness, so UN8IDs also differ if several threads 
in the same system create a UN8ID at exactly the same time.

The use of SHA-256 obscures the original input and still ensures uniqueness based on the input. 
The possibility of additional dynamic input of undefined data, which significantly changes the hash value, 
can also increase anonymity in the context of UN8IDs.

### Advantages over conventional UIDs

Common UIDs usually consist of a timestamp and a random part or the unique IEEE 802 MAC-Address[^5] 
of the network card. Some UIDs are generated completely randomly. [^1]

In the case of UIDs that contain a random component, there is a residual probability of a collision, 
the level of which depends on the frequency of generation and the method used; even if this is so low 
that it is considered negligible in the scientific community. 
UN8ID completely dispenses with random values for identification.

If a unique MAC-Address is used to generate common UIDs, the collision probability is reduced to 0 at global level, 
as long as the local system ensures that UIDs that are generated in the same time unit of the time stamp are modified. 
The disadvantage is that the MAC-Address is clearly present in the generated UID. 
This method is controversial as the MAC-Address is considered a sensitive data.
UN8ID follows a similar approach, but ensures that the MAC-Address cannot be read out.

## Specification

### Versions

#### UN8ID.0
Original specification for maximum physical anonymity.
#### UN8ID.1
Specification for assignable physical uniqueness but anonymized
basic data. Modifications in [Section 3. Component: FINGERPRINT](#section-3-fingerprint).

### Binary Layout and Byte Order

A UN8ID has a fixed length of 384 bits coded in 48 bytes/octets and consists of
8 components divided into 3 sections. Each component is coded in big-endian
format (network byte order).

```
      0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     |               |               |               |               |
TIME +---------------------------------------------------------------+
     | SSE                                                           |
     + - - - - - - - +-----------------------------------------------+
     | ...SSE        | GRANULAR                                      |
     +---------------+ - - - - - - - - - - - - - - - - - - - - - - - +
     | ...GRANULAR                                                   |
META +---------------+---------------+---------------+-+-+-+---------+
     | RCV1          | N_COUNT_BITS  | RCV2          |U|G|S| VERSION |
PHYS +---------------+---------------+---------------+-+-+-+---------+
     | FINGERPRINT                                                   |
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     | ...FINGERPRINT                                                |
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     | ...FINGERPRINT                                                |
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     | ...FINGERPRINT                                                |
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     | ...FINGERPRINT                                                |
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     | ...FINGERPRINT                                                |
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     | ...FINGERPRINT                                                |
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     | ...FINGERPRINT                                                |
     +---------------------------------------------------------------+
```

### Section 1: TIME (bit 0-95/octet 0-11) (96 bits/12 bytes)

Consisting of a timestamp of whole seconds: 40 bits (5 bytes); and a
granulation: 56 bits (7 bytes).

The largest time stamp that can be displayed corresponds to the year 36,812
A.D.

It should be noted that the timestamp and thus UN8ID begins with a null byte
up to a date in the year 2106.

#### Section 1. Component 1: SSE (bit 0-39/octet 0-4) (40 bits/5 bytes)

*(whole) Seconds since Epoch*

The beginning of the epoch is defined analogous to UNIX time [^6] as 
`January 1, 1970, 00:00:00 (UTC)`. This definition is widely recognized in systems and
programming languages.

#### Section 1. Component 2: GRANULAR (bit 40-95/octet 5-11) (56 bits/7 bytes)

Separate from [Section 1. Component 1: SSE](#section-1-component-1-sse-bit-0-39octet-0-4-40-bits5-bytes). 

Consists of granulation of the timestamp based on the resolution of the system clock (real granulation). 

The remaining bits are available to a manual counter whose implementation or format is not defined in 
more detail here (pseudo granulation).

The part of the real granulation must be shifted to the left up to the full bit length of the component, 
taking into account its maximum possible bit length. The resulting bit positions are available for pseudo granulation. 
Their bit length is stored decimal as 1 byte in 
[Section 2, Component 2: N_COUNT_BITS](#section-2-component-2-n_count_bits-bit-104-111octet-13-8-bits1-bytes).

### Section 2: META (bit 96-127/octet 12-15) (32 bits/4 bytes)
Metadata for the UN8ID is stored here. The part of the UN8ID from this section onwards can be temporarily 
stored for a frequent creation and does not have to be recalculated for each UN8ID. 
As long as the basic parameters do not change.

#### Section 2 Component 1: RCV1 (Bit 96-103/Octet 12) (8 Bits/1 Bytes)
Reserved component 1 for extensions in later versions. 
*Currently thought of for an extension of the granulation / sorting parameters.*

#### Section 2. Component 2: N_COUNT_BITS (bit 104-111/octet 13) (8 bits/1 bytes)
The number of free bits for a pseudo granulation in 
[Section 1. Component 2: GRANULAR](#section-1-component-2-granular-bit-40-95octet-5-11-56-bits7-bytes). 
*The lower the decimal value, the more meaningful the granulation.*

#### Section 2. Component 3: RCV2 (bit 112-119/octet 14) (8 bits/1 bytes)
Reserved component 2 for extensions in later versions.

#### Section 2. Component 3: U|G|S| VERSION (Bit 120-127/Octet 15) (8 Bits/1 Bytes)
This octet is composed of:
- `U` Unicast Bit: is set to 1 if the IEEE 802 MAC-Address[^5] used in 
  [Section 3. Component: FINGERPRINT](#section-3-fingerprint) 
  has the unicast/multicast bit set to `0` [^7].
- `G` Global Bit: is set to 1 if the MAC-Address used in 
  [Section 3. Component: FINGERPRINT](#section-3-fingerprint) 
  has the global/local bit set to `0` [^7].
- `S` Standard Bit: is set to 1 if the UN8ID was created based on a standard. 
  Must be `0` for prototypes or modifications.
- `VERSION`: The remaining 5 bits indicate the version of the UN8ID. 
  32 possible decimal values (0-31).

Special definition: If no MAC-Address can be retrieved on systems (e.g. missing network card), 
it is permitted in [Section 3. Component: FINGERPRINT](#section-3-fingerprint) to use a \[pseudo-]random value; 
in this case `U` and `G` must be set to `0`.

### Section 3. Component: FINGERPRINT (Bit 128-383/Octet 16-47) (256 Bits/32 Bytes)

This component represents the physical uniqueness of the UN8ID and consists of 
the result of the SHA-256 function (RFC6234 [^2]).

Here the input is defined.

#### VERSION 0

FINGERPRINT of the original UN8ID specification for highest physical anonymity.

##### Layout for Inputs

Minimum size of 136 bits (17 bytes); up to 160 bits (20 bytes)

```
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 |               |               |               |               |
 +---------------------------------------------------------------+
 | 0 0 0 0 0 0 0 | MAC                                           |
 +---------------+ - - - - - - - - - - - - - - - - - - - - - - - +
 | ...MAC                                                        |
 + - - - - - - - +-----------------------------------------------+
 | ...MAC        | TID                                           |
 +---------------+ - - - - - - - - - - - - - - - - - - - - - - - +
 | ...TID                                                        |
 + - - - - - - - +-----------------------------------------------+
 | ...TID        | ?RND?...?                                     |                                                     
 +---------------+-----------------------------------------------+
```

##### VER (Bit 0-7/Octet 0) (8 bits/1 byte)
`0000 0000` (Version)

##### MAC (Bit 8-71/Octet 1-8) (64 bits/8 bytes)
The IEEE 802 MAC-Address[^5] as a 48-bit integer in big-endian format. 
If no MAC-Address can be retrieved (e.g. missing network card), 
it is permitted to use a \[pseudo-]random value; in this case, `U` and `G` in 
[Section 2. Component 3: U|G|S|VERSION](#section-2-component-3-ugs-version-bit-120-127octet-15-8-bits1-bytes) 
must be set to `0`.

##### TID (Bit 72-135/Octet 9-16) (64 bits/8 bytes)
A Thread-ID unique at lifetime of the thread that creates the UN8ID. 
As this element only has a short-lived meaning, its content is not defined in more detail. 
Nevertheless, its uniqueness in the system must be ensured within the time unit used.

It is recommended to use a native Thread-ID managed by the kernel.

##### RND (Bit 136-159/octet 17-19) (24 bits/3 bytes)
Up to 24 bits (3 bytes) can be appended undefined to the preceding data. 
This element is used for additional anonymization of the origin of a UN8ID within the lifetime of a thread.
The amount was chosen with regard to performance and cryptography 
(more on this in [Security Considerations](#security-considerations)).

#### VERSION 1

FINGERPRINT for an assignable physical uniqueness but anonymized basic data. 
As a Thread-ID is not used in this version, thread safety cannot be guaranteed on this basis. 
This must be implemented at system or process level depending on the use case.

##### Layout for Inputs

Fixed size of 136 bits (17 bytes)


```
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 |               |               |               |               |
 +---------------------------------------------------------------+
 | 0 0 0 0 0 0 1 | MAC                                           |
 +---------------+ - - - - - - - - - - - - - - - - - - - - - - - +
 | ...MAC                                                        |
 + - - - - - - - +-----------------------------------------------+
 | ...MAC        | KEY                                           |
 +---------------+ - - - - - - - - - - - - - - - - - - - - - - - +
 | ...KEY                                                        |
 + - - - - - - - +-----------------------------------------------+
 | ...KEY        |                                                      
 +---------------+ 
```


##### VER (Bit 0-7/Octet 0) (8 bits/1 byte)
`0000 0001` (Version)

##### MAC (Bit 8-71/octet 1-8) (64 bits/8 bytes)
= [VERSION 0](#mac-bit-8-71octet-1-8-64-bits8-bytes)

##### KEY (Bit 72-135/octet 9-16) (64 bits/8 bytes)
Instead of the Thread-ID, a private 64-bit key (undefined) is passed in this version. 
This should be assigned once to one or more MAC-Addresses and stored locally. 
The key is used to defend against brute force attacks, as the MAC-Address alone can be guessed in a few hours.

### Coding
The specified abstraction level for UN8ID is bytes.

For coding in other data types, it should be ensured that the time stamp is available 
separately from the META and FINGERPRINT sections even after coding.

This is the case if the UN8ID is encoded as a whole with base16, base64 or Ascii85. 
However, not with base32, here the TIME section and the META+PHYS sections would have to 
be coded separately without padding and then merged.

## Basic Algorithm

### System check

- Check the system clock for the current time. 

  (e.g. using an NTP query)

- Check whether the system clock uses UNIX time. 
 
  (`beginning of the epoch = January 1, 1970, 00:00:00 (UTC)`) 

  If not, the time in the calculation can be adjusted accordingly.

- Check the resolution of the system clock and calc [N_COUNT_BITS](#section-2-component-2-n_count_bits-bit-104-111octet-13-8-bits1-bytes).

  (`r` = number of decimal places of a second) 
  
  `N_COUNT_BITS = 56 - int(r x log2(10) + 1)`

  (Maximum permitted value for the pseudo-granular counter = $2^{N\ COUNT\ BITS}-1$ )

- If not identical, check the resolution of the system time that can be retrieved from the system.
  
  (`r` = number of decimal places of a second):

  `GRANULAR_LEFT_PADDING_SHIFT = 56 - int(r x log2(10) + 1)`

- Otherwise:
  
  `GRANULAR_LEFT_PADDING_SHIFT = N_COUNT_BITS`
  
- Check whether a MAC-Address can be queried by the system and save its characteristics. 

  ([Section 2. Component 3: U|G|S|VERSION](#section-2-component-3-ugs-version-bit-120-127octet-15-8-bits1-bytes))

  `MAC-ID = int.base16(MAC-Address)`

  `first_byte = MAC-ID >> 40`

  `U = not first_byte & 0b00000001`

  `G = not first_byte & 0b00000010`

- Otherwise, a randomly generated 48 bit number can be used, then:
  
  `U = 0`
  
  `G = 0`
  
- If as recommended for [Section 3. Component: FINGERPRINT Version 0](#version-0) 
  a native Thread-ID managed by the kernel is required, check whether the system assigns Thread-IDs in this way.

- If random values are used in some place, check whether a cryptographically secure method is available in the system.

### Section 1: [TIME](#section-1-time-bit-0-95octet-0-11-96-bits12-bytes)
- Format whole seconds in 5 bytes in big-endian format and write them to the buffer ([SSE](#section-1-component-1-sse-bit-0-39octet-0-4-40-bits5-bytes)).
- Shift the time granular by `GRANULAR_LEFT_PADDING_SHIFT` to the left and insert the value from the pseudo-granular 
  counter with bitwise OR
  ([GRANULAR](#section-1-component-2-granular-bit-40-95octet-5-11-56-bits7-bytes)).
  Format the value in 7 bytes in big-endian format and write them to the buffer.

### Section 2: [META](#section-2-meta-bit-96-127octet-12-15-32-bits4-bytes)
- Write a zero byte to the buffer ([RSV1](#section-2-component-1-rcv1-bit-96-103octet-12-8-bits1-bytes)).
- Format [N_COUNT_BITS](#section-2-component-2-n_count_bits-bit-104-111octet-13-8-bits1-bytes) to 1 byte in big-endian format and write it to the buffer.
- Write a zero byte to the buffer ([RSV2](#section-2-component-3-rcv2-bit-112-119octet-14-8-bits1-bytes)).
- Shift `U` 7 positions to the left, shift `G` 6 positions to the left, shift `S` 5 positions to the left and merge with 
  the `VERSION` number using bitwise OR
  ([U|G|S|VERSION](#section-2-component-3-ugs-version-bit-120-127octet-15-8-bits1-bytes)).
  Format the value in 1 byte in big-endian format and write it to the buffer.

### Section 3: [FINGERPRINT](#section-3-component-fingerprint-bit-128-383octet-16-47-256-bits32-bytes)
- Create a temporary buffer.
- Format the version number in 1 byte in big-endian format and write it to the temp. buffer.
- Format the MAC ID in 8 bytes in big-endian format and write it to the temp. buffer.
- [@VERSION 0](#version-0):
  - Query the current Thread-ID and format it in 8 bytes in big-endian format and write it to the temp. buffer.
  - (Optional) Write the additional data to the temp. buffer.
- [@VERSION 1](#version-1):
  - Format the personal key in 8 bytes in big-endian format and write it to the temp. buffer.
- Generate an SHA-256 value from the temp. buffer and write it to the main buffer.


## Security Considerations

### Correlation between secure obfuscation of the MAC-Address and collision probability in FINGERPRINT
_The problem_: the greater the number of possible inputs, the more difficult it is to guess them, 
but at the same time the probability of collisions also increases.

Therefore, it is necessary to increase the number of possible inputs to a value that makes 
a brute force attack pointless, but at least respects the Pigeonhole Principle[^9]. 
Assuming that SHA-256 distributes inputs completely homogeneously, 
the collision probability is really 0 according to the Pigeonhole Principle.

### Duration $d$ of a brute force attack against the FINGERPRINT to find the MAC-Address
It is assumed that half of all possible calculations $n$ must be performed before a match is made.

$$
d = \frac{\frac{n}{2}}{hr}
$$

- *Scenario 1*: The currently (2025) most powerful hardware with a hash rate $hr \approx 10^{9} \space \text{h/s}$ is used for the attack.
- *Scenario 2*: Hardware with a hash rate $hr = 10^{12} \space \text{h/s}$ is used for the attack.

#### @VERSION 0:
Assumptions: Every possible MAC-Address in the space of $2^{48}$ 
$\times$ every possible Thread-ID in the space of $2^{31}$ must potentially be checked 
and no additional data has been appended to the input.

$n = 2^{48} \times 2^{31} = 2^{79} = 6 \times 10^{23}$
- *Scenario 1*: $d \approx 9,000,000 \space \text{years}$
- *Scenario 2*: $d \approx 9,000 \space \text{years}$

#### @VERSION 1:
Assumptions: Every possible MAC-Address in the space of $2^{48}$
$\times$ every possible key in the space of $2^{64}$ must potentially be checked.

$n = 2^{48} \times 2^{64} = 2^{112} = 5 \times 10^{33}$
- *Scenario 1*: $d \approx 8 \times 10^{16} \space \text{years}$
- *Scenario 2*: $d \approx 8 \times 10^{13} \space \text{years}$

### Collision probabilities
Here, the probability of a collision is treated in isolation for the physical part of a UN8ID 
on the basis of the Birthday Problem. 
Other parameters of the UN8ID significantly reduce the probability for a UN8ID as a whole. 
In addition, the Pigeonhole Principle[^9] is always respected when specifying the versions of UN8ID. 
The number of possible entries for the FINGERPRINT should not exceed the size of the hash space of SHA-256 ($2^{256}$).

Birthday Problem[^8] formula:

$$
P(n) = 1 - e^{-\frac{n(n-1)}{2N}}
$$

- $P(n)$: Probability of collision `0...1` (`0%...100%`)
- $n$: Number of possible inputs
- $N$: Number of possible results = $2^{256}$ for SHA-256
- $e$: Euler's number (exponential function)

#### @VERSION 0:
$n = 2^{48} \times 2^{31} = 2^{79} = 6 \times 10^{23}$

$P(n) = 0.0 \space \text{(cannot be calculated)}$

#### @VERSION 1:
$n = 2^{48} \times 2^{64} = 2^{112} = 5 \times 10^{33}$

$P(n) \approx 1.165 \times 10^{-10}$ (0.000,000,011,65 %)



## Appendix A: Prototype Implementation

src: [prototype.py](https://github.com/UN8ID/UN8ID/blob/master/src/UN8ID/prototype.py)


```python
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
```


## Appendix B: Application Sample

src: [prototype.py](https://github.com/UN8ID/UN8ID/blob/master/src/UN8ID/prototype.py)


```python
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
```


## Appendix C: Demo

src: [prototype.py](https://github.com/UN8ID/UN8ID/blob/master/src/UN8ID/prototype.py)


```python
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
```


## Appendix D: Sample Demo Output

```
===================
UN8ID.0 (no count, no add. data)
                  b'\x00g\x8eM\x91E\xa6\xf6P\x00\x00\x00\x00\x1a\x00\xc0v\x84\x1cHj0\x8e\x96\xbf\xe1\x95\x9a\xe6=&\xe7T\xfd\x8a\x94\xdb9\x92\xe5\xb5.]w\x11\xef\x08G'
  ~hex            : 00678e4d9145a6f650000000001a00c076841c486a308e96bfe1959ae63d26e754fd8a94db3992e5b52e5d7711ef0847
  ~base64         : AGeOTZFFpvZQAAAAABoAwHaEHEhqMI6Wv+GVmuY9JudU/YqU2zmS5bUuXXcR7whH
-------------------
    .SSE          : 1,737,379,217
      ~date       : 2025-01-20 13:20:17+00:00
    .GRANULAR     : 196,053,502,273,781,76
      ~bits       : 0b1000101101001101111011001010000000000000000000000000000
      .real       : 292,142,484
      .pseudo     : 0
    .RCV1         : 0
    .N_COUNT_BITS : 26
    .RCV2         : 0
    .VERSION      : 192
      .U          : 1
      .G          : 1
      .S          : 0
      .VERSION    : 0
    .FINGERPRINT  : b'v\x84\x1cHj0\x8e\x96\xbf\xe1\x95\x9a\xe6=&\xe7T\xfd\x8a\x94\xdb9\x92\xe5\xb5.]w\x11\xef\x08G'
      ~hex        : 76841c486a308e96bfe1959ae63d26e754fd8a94db3992e5b52e5d7711ef0847
===================


===================
UN8ID.1 (no count, no key)
                  b'\x00g\x8eM\x91E\xe5\x15\xf8\x00\x00\x00\x00\x1a\x00\xc1????????????????????????????????'
  ~hex            : 00678e4d9145e515f8000000001a00c13f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f
  ~base64         : AGeOTZFF5RX4AAAAABoAwT8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/
-------------------
    .SSE          : 1,737,379,217
      ~date       : 2025-01-20 13:20:17+00:00
    .GRANULAR     : 196,736,559,108,587,52
      ~bits       : 0b1000101111001010001010111111000000000000000000000000000
      .real       : 293,160,318
      .pseudo     : 0
    .RCV1         : 0
    .N_COUNT_BITS : 26
    .RCV2         : 0
    .VERSION      : 193
      .U          : 1
      .G          : 1
      .S          : 0
      .VERSION    : 1
    .FINGERPRINT  : b'????????????????????????????????'
      ~hex        : 3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f
===================


===================
UN8ID.0 (count, add. data)
                  b'\x00g\x8eM\x91E\xe8E\x84\x00\x00\x01\x00\x1a\x00\xc0\xedlG>\xe3\x17N\xb8c\xa6+\xf9b\x8f|\xb7\xfe\x03\xbfL9\x84\xa8,\x90Z\x13\xf0\xfe\x17\xa0\xdb'
  ~hex            : 00678e4d9145e84584000001001a00c0ed6c473ee3174eb863a62bf9628f7cb7fe03bf4c3984a82c905a13f0fe17a0db
  ~base64         : AGeOTZFF6EWEAAABABoAwO1sRz7jF064Y6Yr+WKPfLf+A79MOYSoLJBaE/D+F6Db
-------------------
    .SSE          : 1,737,379,217
      ~date       : 2025-01-20 13:20:17+00:00
    .GRANULAR     : 196,771,586,580,152,33
      ~bits       : 0b1000101111010000100010110000100000000000000000000000001
      .real       : 293,212,513
      .pseudo     : 1
    .RCV1         : 0
    .N_COUNT_BITS : 26
    .RCV2         : 0
    .VERSION      : 192
      .U          : 1
      .G          : 1
      .S          : 0
      .VERSION    : 0
    .FINGERPRINT  : b'\xedlG>\xe3\x17N\xb8c\xa6+\xf9b\x8f|\xb7\xfe\x03\xbfL9\x84\xa8,\x90Z\x13\xf0\xfe\x17\xa0\xdb'
      ~hex        : ed6c473ee3174eb863a62bf9628f7cb7fe03bf4c3984a82c905a13f0fe17a0db
===================


===================
UN8ID.1 (count, key)
                  b'\x00g\x8eM\x91E\xebR4\x00\x00\x02\x00\x1a\x00\xc1\xafr\x98\xd3\xf9N\x9f\xb6Z/\x1aV\xace\xa5\x16\xab\x87[v\xf5\xdbh\x810\x03>\x7fV\xed\x02>'
  ~hex            : 00678e4d9145eb5234000002001a00c1af7298d3f94e9fb65a2f1a56ac65a516ab875b76f5db688130033e7f56ed023e
  ~base64         : AGeOTZFF61I0AAACABoAwa9ymNP5Tp+2Wi8aVqxlpRarh1t29dtogTADPn9W7QI+
-------------------
    .SSE          : 1,737,379,217
      ~date       : 2025-01-20 13:20:17+00:00
    .GRANULAR     : 196,805,116,852,961,30
      ~bits       : 0b1000101111010110101001000110100000000000000000000000010
      .real       : 293,262,477
      .pseudo     : 2
    .RCV1         : 0
    .N_COUNT_BITS : 26
    .RCV2         : 0
    .VERSION      : 193
      .U          : 1
      .G          : 1
      .S          : 0
      .VERSION    : 1
    .FINGERPRINT  : b'\xafr\x98\xd3\xf9N\x9f\xb6Z/\x1aV\xace\xa5\x16\xab\x87[v\xf5\xdbh\x810\x03>\x7fV\xed\x02>'
      ~hex        : af7298d3f94e9fb65a2f1a56ac65a516ab875b76f5db688130033e7f56ed023e
===================


===================
UN8ID.1 (count, key) (another)
                  b'\x00g\x8eM\x91E\xed\xae\x8c\x00\x00\x03\x00\x1a\x00\xc1\xafr\x98\xd3\xf9N\x9f\xb6Z/\x1aV\xace\xa5\x16\xab\x87[v\xf5\xdbh\x810\x03>\x7fV\xed\x02>'
  ~hex            : 00678e4d9145edae8c000003001a00c1af7298d3f94e9fb65a2f1a56ac65a516ab875b76f5db688130033e7f56ed023e
  ~base64         : AGeOTZFF7a6MAAADABoAwa9ymNP5Tp+2Wi8aVqxlpRarh1t29dtogTADPn9W7QI+
-------------------
    .SSE          : 1,737,379,217
      ~date       : 2025-01-20 13:20:17+00:00
    .GRANULAR     : 196,831,073,219,379,23
      ~bits       : 0b1000101111011011010111010001100000000000000000000000011
      .real       : 293,301,155
      .pseudo     : 3
    .RCV1         : 0
    .N_COUNT_BITS : 26
    .RCV2         : 0
    .VERSION      : 193
      .U          : 1
      .G          : 1
      .S          : 0
      .VERSION    : 1
    .FINGERPRINT  : b'\xafr\x98\xd3\xf9N\x9f\xb6Z/\x1aV\xace\xa5\x16\xab\x87[v\xf5\xdbh\x810\x03>\x7fV\xed\x02>'
      ~hex        : af7298d3f94e9fb65a2f1a56ac65a516ab875b76f5db688130033e7f56ed023e
===================
```







<hr>

[^1]: https://en.wikipedia.org/wiki/Universally_unique_identifier

[^2]: https://github.com/ulid/spec

[^3]: https://en.wikipedia.org/wiki/Instructions_per_second

[^4]: https://www.rfc-editor.org/rfc/rfc6234

[^5]: https://standards.ieee.org/wp-content/uploads/import/documents/tutorials/macgrp.pdf

[^6]: https://en.wikipedia.org/wiki/Unix_time

[^7]: https://en.wikipedia.org/wiki/MAC_address#Unicast_vs._multicast

[^8]: https://en.wikipedia.org/wiki/Birthday_problem

[^9]: https://en.wikipedia.org/wiki/Pigeonhole_principle


