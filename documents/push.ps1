npm run docs:build
sleep(1)
del ..\docs -recurse
sleep(1)
echo d | xcopy .\docs\.vuepress\dist ..\docs /E
