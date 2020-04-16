@echo off
echo Re-HASH CRC64
set startTime=%time%
call "C:\Program Files\7-Zip\7z.exe" h -scrcCRC64 > re-hash.txt
echo Start  Time: %startTime%
echo Finish Time: %time%
