# Perfcheck

- [source (not available)](http://castle.cse.ust.hk/perfchecker/tool_obtain.php)
- [paper](https://dl.acm.org/doi/pdf/10.1145/2568225.2568229)
- language: Java 6 (works with 7, probably better because dex2jar oldest release is also java 7)
- number of years without at least 1 commit since first commit: ?
- License: Proprietary

## Notes

The binary is only available on demand, so we don't provide it ourself. We can still provide the dockerfile, which will only build if provided with the provided .jar.
To make sure the same .jar we used are provided, there checksum is provided and checked in the dockerfile (cf `checksums.sha256`).

The bytecode to analyse must be convert to java bytecode and loaded as code (with `-cp`), as does the `android.jar`. This means that the supported android version are limited by the java version (`Unsupported major.minor version` errors for android.jar >= sdk 24)
