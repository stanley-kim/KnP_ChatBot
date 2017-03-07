cf ssh wskSidney -c "cat app/static/organization.txt" > res_org.txt
find /c "FAILED" res_org.txt
if %errorlevel% equ 1 goto notfound
echo FAILED found
goto dopush
:notfound
echo FAILED notfound
cf ssh wskSidney -c "cat app/static/organization.txt" > static/organization.txt
goto dopush
:dopush
del res_org.txt
cf push wskSidney

