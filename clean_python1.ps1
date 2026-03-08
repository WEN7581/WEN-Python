# 清理pip缓存
python -m pip cache purge

# 更新所有包（减少旧版本占用）
pip list --outdated --format=freeze | ForEach-Object { 
    $package =$_.Split("==")[0]
    pip install --upgrade $package
}

# 删除.pyc缓存文件
Get-ChildItem "D:\Program Files\Python313" -Recurse -Filter "*.pyc" | Remove-Item
Get-ChildItem "D:\Program Files\Python313" -Recurse -Filter "__pycache__" -Directory | Remove-Item -Recurse

Write-Host "清理完成！" -ForegroundColor Green