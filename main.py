import subprocess

def run_python_script(script_name):
    subprocess.run(["python3", script_name], check=True)

def news_crawler():
    # scripts_to_run = ["get_incremental.py","db.py", "g_news.py", "upload_db.py"]
    scripts_to_run = ["wangyi.py", "dongfangcaifu.py", "hexun.py", "tencent.py", "wallstreetcn.py", "sina.py"]
    for script in scripts_to_run:
        try:
            print("We are running: " + script)
            run_python_script(script)
            print(f"Successfully executed: {script}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing {script}: {e}")
            # Optionally, you can raise an exception here to stop execution in case of any script failure.
            # raise

    return "All scripts executed successfully."


# Uncomment the next line for local testing (outside of Lambda environment).
news_crawler()
# keyword = 'superconductor'