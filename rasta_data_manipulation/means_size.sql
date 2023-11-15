SELECT AVG(dex_size) FROM apk;
SELECT AVG(dex_size) FROM apk WHERE vt_detection = 0;
SELECT AVG(dex_size) FROM apk WHERE vt_detection != 0;
SELECT AVG(apk_size) FROM apk;
SELECT AVG(apk_size) FROM apk WHERE vt_detection = 0;
SELECT AVG(apk_size) FROM apk WHERE vt_detection != 0;
