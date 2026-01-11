def handle_job(job):
    job_type = job["type"]
    if(job_type == "send_email"):
        send_email(job["payload"])
    else:
        raise ValueError(f"Invalid job type: {job_type}")
    
def send_email(payload):
    print(f"Sending email to {payload['to']}")