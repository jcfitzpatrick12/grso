import subprocess

def main():

    #from gui.LookBetween import LookBetween
    subprocess.run(['python3', 'gui/SetBackground.py', '00'])
    # subprocess.run(['python3', 'gui/LookBetween.py', '00'])
    # subprocess.run(['bash', 'run_observations/batch/batch_observe.sh', '2', '10', '03'])
    # subprocess.run(['bash', 'callisto/web_fetch.sh'])
    pass

if __name__ == "__main__":
    main()