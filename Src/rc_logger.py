# import: std
import os
import logging

# import: non-std

# import: locals

# globals/const

# main
def main():
    pass

# code blocks

def logger() -> logging.Logger:
    
    env_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'.env')
    log_path = os.path.join(env_dir,'env.log')
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)

    logging.basicConfig(
        filemode="w",
        # filename=os.path.join(file_dir, "rc_logger.log"),
        filename=log_path,
        style="{",
        format="[{levelname}: {processName}: {threadName}: {module}: {funcName}: \n\t{message}]",
        level=logging.DEBUG,
    )
    log = logging.getLogger()
    return log

# logic
if __name__ =='__main__':
    main()