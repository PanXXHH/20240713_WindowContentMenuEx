@echo off
echo 检查当前Git状态...
git status
echo.

:confirm
set /p response=是否继续添加所有文件并提交？(y/n):
if /i "%response%"=="y" goto add
if /i "%response%"=="n" goto end
echo 请输入y或n。
goto confirm

:add
set /p changeinfo=请输入提交信息:
git add .
git commit -m "%changeinfo%"
if %errorlevel% neq 0 goto error

echo 尝试推送到远程仓库...
git push
if %errorlevel% neq 0 goto error

echo 提交和推送成功！
goto end

:error
echo 发生错误，操作未完成。
goto end

:end
pause
