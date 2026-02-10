import logging

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

def log(user, action):
    logging.info(f"user={user} action={action}")
