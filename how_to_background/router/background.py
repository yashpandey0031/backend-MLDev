#tasks that happen in background like in a account created email when the account is created

from fastapi import BackgroundTasks

def send_welcome_email(username:  str):
  print(f"sending welcome email to { username}")


@router.post("/register")
def register(username: str, background_task: BackgroundTasks, db: Session = Depends(get_db)):
  background_task.add_task(send_welcome_email, username)
  return {"message": "Account created"}
