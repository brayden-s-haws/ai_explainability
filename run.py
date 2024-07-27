import multiprocessing
import os
import streamlit.web.bootstrap

def run_streamlit():
    os.system("streamlit run app.py")

if __name__ == "__main__":
    multiprocessing.Process(target=run_streamlit).start()

    # Keep the main process running
    streamlit.web.bootstrap.run(app_file="app.py", command_line="", args=[], flag_options={})
