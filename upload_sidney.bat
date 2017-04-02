
copy manifest_sidney.yml manifest.yml /Y
copy runtime_sidney.txt  runtime.txt  /Y
copy README_sidney.md    README.md    /Y

cf ssh wskSidney -c "cat app/static/organization.txt" > res_org_sidney.txt
find /c "FAILED" res_org_sidney.txt
if %errorlevel% equ 1 goto notfound
echo FAILED found
goto dopush
:notfound
echo FAILED notfound
cf ssh wskSidney -c "cat app/static/organization.txt" > static/organization_sidney.txt
copy static\organization_sidney.txt static\organization.txt /Y
copy static\contact_list_sidney.txt static\contact_list.txt /Y
goto dopush
:dopush
del res_org_sidney.txt
cf push wskSidney

