echo off

set update_file="dummy"

@if "%1"=="" (
  echo "[stop] Require argument: path(git clone directory)"
  exit /b
) else (
  set git_clone_path=%1
)

cd %git_clone_path%

echo "dummy update: %date%" >%update_file%
git add %update_file%
git commit -m "dummy update: %date%"
git push
