import tempfile


with tempfile.TemporaryDirectory() as tmp_dir1:
    print("created directory", tmp_dir1)


tmp_dir2 = tempfile.mkdtemp()
print("created directory", tmp_dir2)
