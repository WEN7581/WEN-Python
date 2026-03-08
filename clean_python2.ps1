# clean_python.ps1
Write-Host "=== Python包清理工具 ===" -ForegroundColor Cyan

# 1. 清理pip缓存
Write-Host "清理pip缓存..." -ForegroundColor Yellow
python -m pip cache purge

# 2. 列出最大的包
Write-Host "`n最大的10个包：" -ForegroundColor Yellow
$packages = Get-ChildItem "D:\Program Files\Python313\Lib\site-packages" -Directory | ForEach-Object {$size = (Get-ChildItem $_.FullName -Recurse | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{
        Package =$_.Name
        SizeMB = [math]::Round($size / 1MB, 2)
    }
} | Sort-Object SizeMB -Descending | Select-Object -First 10$packages | Format-Table -AutoSize

# 3. 询问是否卸载
$toRemove = Read-Host "`n输入要卸载的包名（用空格分隔），或按Enter跳过"
if ($toRemove) {$toRemove.Split(" ") | ForEach-Object {
        Write-Host "卸载 $_..." -ForegroundColor Yellow
        pip uninstall -y$_
    }
}

# 4. 清理.pyc文件
Write-Host "`n清理.pyc缓存文件..." -ForegroundColor Yellow
Get-ChildItem "D:\Program Files\Python313" -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem "D:\Program Files\Python313" -Recurse -Filter "__pycache__" -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force

Write-Host "`n清理完成！" -ForegroundColor Green