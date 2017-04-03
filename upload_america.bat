
copy manifest_america.yml manifest.yml /Y
copy runtime_america.txt  runtime.txt  /Y
copy README_america.md    README.md    /Y

cf ssh wskars -c "cat app/static/organization.txt" > res_org_america.txt
find /c "FAILED" res_org_america.txt
if %errorlevel% equ 1 goto notfound
echo FAILED found
goto dopush
:notfound
echo FAILED notfound
cf ssh wskars -c "cat app/static/organization.txt" > static/organization_america.txt
copy static\organization_america.txt static\organization.txt /Y
copy static\contact_list_america.txt static\contact_list.txt /Y
copy static\document_america.txt     static\document.txt /Y
goto dopush
:dopush
del res_org_america.txt
cf push wskars

