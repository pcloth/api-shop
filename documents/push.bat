@ECHO OFF&PUSHD %~DP0
rem 请将qingruan.tech项目和qingruan.admin项目放在同一目录
%1 %2
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :runas","","runas",1)(window.close)&goto :eof
:runas
Powershell.exe -executionpolicy remotesigned -File %~dp0\push.ps1
prase